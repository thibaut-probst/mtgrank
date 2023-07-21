from argparse import ArgumentParser, RawTextHelpFormatter
from rich.prompt import Prompt
from rich.progress import Progress
from datetime import datetime, timedelta
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from re import compile


def crawl_event(url, mtg_source, mtg_format, algo):
    '''
    MTG event crawling function
        
            Parameters:
                url (str): event url
                mtg_source (str): MTG data source
                mtg_format (str): MTG format
                algo (str): ranking algorithm
            Returns:
                deck_ranking (dict): event deck ranking
    ''' 

    deck_ranking = {}

    user_agent = {'User-agent': 'Mozilla/5.0'}

    # Send an HTTP GET request to the URL
    response = get(url, headers = user_agent)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Process the HTML content
        links = soup.find_all('a')

        # Look for the number of players in the tournament, if not found set it to 8
        nb_players = 8

        if (mtg_source == 'mtgtop8'):
            nb_players_regex = compile('([0-9]+) players')
        elif mtg_source == 'mtgdecks':
            nb_players_regex = compile('([0-9]+) Players')
        elif mtg_source == 'mtggoldfish':
            if 'Displaying <b>all' in response.text:
                nb_players_regex = compile('Displaying <b>all&nbsp;([0-9]+)<\/b> decks')
            else:
                nb_players_regex = compile(' of <b>([0-9]+)<\/b> in total')

        try:
            nb_players = int(nb_players_regex.findall(response.text)[0])
        except:
            pass

        decks = []
        for link in links:
            # Find all the links on the page
            href = link.get('href')
            txt = link.text
            if href and txt:
                href = href.lower()
                # Only keep deck archetypes
                if (len(txt) > 1) and (not 'Winrates' in txt):
                    if (href.startswith('?e=') and href.endswith(f'&f={mtg_format[0:2]}')) or\
                        (href.startswith(f'/{mtg_format}/') and (not href.startswith(f'/{mtg_format}/tournaments')) and (not href.startswith(f'/{mtg_format}/staples')) and (not href.startswith('/{mtg_format}/winrates'))) or\
                        (href.startswith('/deck/') and (not href.startswith('/deck/custom/')) and (not href.startswith('/deck/visual/'))):
                            # Merge similar archetypes
                            if ('Creativi' in txt) or ('Idomitab' in txt):
                                txt = 'Creativity'
                            elif 'Affinity' in txt:
                                txt = 'Affinity'
                            elif ('urktid' in txt) or ('Izzet Midrange' in txt):
                                txt = 'UR Murktide'
                            elif 'Mill' in txt:
                                txt = 'Mill'
                            elif 'Temur' in txt:
                                txt = 'Temur Cascade'
                            elif ('Omnath' in txt) or ('4c Control' in txt) or ('Elemental' in txt):
                                txt = '4cc'
                            elif ('Yawgmoth' in txt) or ('Chord Toolbox' in txt):
                                txt = 'Yawgmoth Evolution'
                            elif 'Burn' in txt:
                                txt = 'Burn'
                            elif 'Tron' in txt:
                                txt = 'Tron'
                            elif 'Hammer' in txt:
                                txt = 'Hammer Time'
                            elif ('Rakdos' in txt) or ('Rb Scam' in txt):
                                txt = 'Rakdos'
                            elif 'Green Devotion' in txt:
                                txt = 'Green Devotion'
                            elif 'Death' in txt:
                                txt = 'Grixis Death\'s Shadow'
                            decks.append(txt)
    
    # Ranking
    deck_pos = 1
    for deck in decks:
        pts = 0

        # Only TOP8
        if deck_pos > 8:
            break

        # Points calculation according to algorithm
        if algo == 'exponential':
            if deck_pos == 1:
                pts = 8 * int(round(nb_players / 8, 0))
            elif deck_pos == 2:
                pts = 4 * int(round(nb_players / 8, 0))
            elif (deck_pos == 3) or (deck_pos == 4):
                pts = 2 * int(round(nb_players / 8, 0))
            elif deck_pos > 4:
                pts = 1 * int(round(nb_players / 8, 0))
        elif algo == 'linear':
            pts = (9-deck_pos) * int(round(nb_players / 8, 0))

        if deck not in deck_ranking.keys():
            deck_ranking[deck] = [pts, 1]
        else:
            deck_ranking[deck] = [deck_ranking[deck][0] + pts, deck_ranking[deck][1]+1]
        
        deck_pos += 1

    return deck_ranking


def crawl_source(url, mtg_source, mtg_format, mtgdecks_date, algo):
    '''
    MTG source crawling function
        
            Parameters:
                url (str): event url
                mtg_source (str): MTG data source
                mtg_format (str): MTG format
                mtgdecks_date (datetime.date): date to look up to
                algo (str): ranking algorithm
            Returns:
                global_deck_ranking (dict): global deck ranking
    '''

    global_deck_ranking = {}
    user_agent = {'User-agent': 'Mozilla/5.0'}
    
    p = 1
    i = 0

    with Progress() as progress:
        task = progress.add_task(f'Parsing {mtg_source.upper()}...', total=100, visible=True)

        completed = 0

        today = datetime.now()
        previous_date = today
        total_period = today - mtgdecks_date

        # Loop until we hit a page with no more event links or the date is passed
        while True:

            # Send an HTTP GET request to the URL
            response = get(f'{url}{p}', headers = user_agent)
            
            # Check if the request was successful
            if response.status_code == 200:
                
                # Parse the HTML content
                resp = response.text
                body = resp
                if mtg_source == 'mtgtop8':
                    try:
                        body = resp.split('LAST 20 EVENTS')[1]
                    except:
                        body = resp.split('align=center>Events ')[1]

                # For MTGGOLDFISH: check if no more events
                if (mtg_source == 'mtggoldfish') and ( ('No tournaments found.' in body) or ('Throttled' in body) ):
                    break
                
                soup = BeautifulSoup(body, 'html.parser')

                # Estimate progress

                events_before_date = []
                # For MTGDECKS, check event dates but also not to parse events over time range
                if mtg_source == 'mtgdecks':
                    event_dates = soup.find_all('strong') # Dates are within strong HTML elements
                    oldest_event_date = None
                    event_before_date = False
                    for event_date_raw in event_dates: 
                        if ('-' in event_date_raw.text) and (len(event_date_raw.text) < 7): # Only keep dates
                            event_date = datetime.strptime(event_date_raw.text, '%d-%b').replace(year=datetime.now().year)
                            if event_date < mtgdecks_date:
                                event_before_date = True
                        if event_before_date:
                            events_before_date.append(event_date_raw.text)
                        else:
                            oldest_event_date = event_date # Keep oldest event date
                    if oldest_event_date:       
                        new_period = previous_date - oldest_event_date # Calculate new progress
                        period_progress = round((new_period / total_period) * 100, 0)
                        previous_date = oldest_event_date

                # For MTGTOP8, check event dates
                elif mtg_source == 'mtgtop8':
                    # Specific date provided, check event dates but also not to parse events over time range
                    if '&meta=44' in url:
                        event_dates = compile('[0-9]+\/[0-9]+\/[0-9]+').findall(body) # Dates are within strong HTML elements
                        oldest_event_date = None
                        event_before_date = False
                        for event_date_raw in event_dates: 
                            event_date = datetime.strptime(event_date_raw, '%d/%m/%y')
                            if event_date < mtgdecks_date:
                                event_before_date = True
                            if event_before_date:
                                events_before_date.append(event_date_raw)
                            else:
                                oldest_event_date = event_date # Keep oldest event date
                        if oldest_event_date:       
                            new_period = previous_date - oldest_event_date # Calculate new progress
                            period_progress = round((new_period / total_period) * 100, 0)
                            previous_date = oldest_event_date
                    # Else just check event dates
                    else:
                        date_regex = compile('[0-9]{2}/[0-9]{2}/[0-9]{2}')
                        matched_dates = soup.find_all(string=date_regex)
                        oldest_event_date_str = matched_dates[-1].string # Keep oldest event date
                        oldest_event_date = datetime.strptime(oldest_event_date_str, '%d/%m/%y') # Take last event date of the page
                        new_period = previous_date - oldest_event_date # Calculate new progress
                        period_progress = round((new_period / total_period) * 100, 0)
                        previous_date = oldest_event_date
                
                # For MTGGOLDFISH, check event dates
                elif mtg_source == 'mtggoldfish':
                    date_regex = compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
                    matched_dates = soup.find_all(string=date_regex)
                    for m in matched_dates:
                        if not m.startswith('20'):
                            matched_dates.remove(m)
                    oldest_event_date_str = matched_dates[-1].string
                    oldest_event_date = datetime.strptime(oldest_event_date_str, '%Y-%m-%d') # Keep oldest event date
                    new_period = previous_date - oldest_event_date # Calculate new progress
                    period_progress = round((new_period / total_period) * 100, 0)
                    previous_date = oldest_event_date

                # Find all the links on the page to look for events
                links = soup.find_all('a')
                events = []

                for link in links:
                    href = link.get('href')

                    if href:
                        href = href.lower()
                        # Only keep event links
                        if ((mtg_source == 'mtgtop8') and href.startswith('event?e=') and href.endswith(f'={mtg_format.lower()[0:2]}') and ((link.text not in events_before_date))) \
                            or ((mtg_source == 'mtgdecks') and href.startswith(f'/{mtg_format}/') and (not href.startswith(f'/{mtg_format}/tournaments')) and (not href.startswith(f'/{mtg_format}/staples')) and (not href.startswith(f'/{mtg_format}/winrates')) and ((link.text not in events_before_date)))\
                            or ((mtg_source == 'mtggoldfish') and href.startswith('/tournament/')):
                                events.append(href)
                
                deck_ranking_event = {}

                events = list(set(events)) # Avoid duplicates

                # Crawl events
                for event in events:
                    if mtg_source == 'mtgtop8':
                        deck_ranking_event = crawl_event(f'https://mtgtop8.com/{event}', mtg_source, mtg_format, algo)
                    elif mtg_source == 'mtgdecks':
                        deck_ranking_event = crawl_event(f'https://mtgdecks.net/{event}', mtg_source, mtg_format, algo)
                    elif mtg_source == 'mtggoldfish':
                        #sleep(1) # Slow down the requests?
                        deck_ranking_event = crawl_event(f'https://www.mtggoldfish.com/{event}', mtg_source, mtg_format, algo) 

                    for deck in deck_ranking_event.keys():
                        pts = deck_ranking_event[deck][0]
                        timestop8 = deck_ranking_event[deck][1]
                        if deck not in global_deck_ranking.keys():
                            global_deck_ranking[deck] = [pts, timestop8]
                        else:
                            global_deck_ranking[deck] = [global_deck_ranking[deck][0]+pts, global_deck_ranking[deck][1]+timestop8]
                
                    progress.update(task, advance=period_progress / len(events))

                # For MTGTOP8 and MTGDECKS: check if no more events
                if ((mtg_source == 'mtgtop8') and ((('<div class=Nav_PN_no>Next</div>' in body) or event_before_date )))\
                    or ( (mtg_source == 'mtgdecks') and event_before_date ):
                    break
            
            else:
                break

            p = p+1

        progress.update(task, completed=100)
        progress.update(task, visible=False)
        progress.remove_task(task)

    return global_deck_ranking             


if __name__ == '__main__':
    
    # Argument parsing from command-line
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        '--source', '-s',
        type = str,
        action = 'store',
        default = 'mtgtop8',
        help = 'Data source to use (mtgtop8, mtgdecks, mtggoldfish ; default: mtgtop8)'
    )

    parser.add_argument(
        '--format', '-f',
        type = str,
        action = 'store',
        default = 'modern',
        help = 'Format (modern, legacy, pioneer ; default: modern)'
    )

    parser.add_argument(
        '--algorithm', '-a',
        type = str,
        action = 'store',
        default = 'exponential',
        help = 'Ranking algorithm (default: exponential):\n\
    Linear: each TOP8 member gets ( (9-n) * nb_players / 8 ) pts, where n is the rank; or\n\
    Exponential: TOP1 gets (8 * nb_players / 8) pts, TOP2 gets (4 * nb_players / 8) pts, TOP3-4 get (2 * nb_players / 8) pts, TOP5-8 get (1 * nb_players / 8) pts'
    )

    parser.add_argument(
        '--top', '-t',
        type = int,
        action = 'store',
        default = 20,
        help = 'TOP ranking size (default: 20)'
    )

    parser.add_argument(
        '--date', '-d',
        action = 'store_true',
        help = 'Time range to be specified through a selection menu (default: last 2 weeks)'
    )

    args = vars(parser.parse_args())

    mtg_source = args['source']
    allowed_sources = ['mtgtop8', 'mtgtop8.com', 'mtgdecks', 'mtgdecks.net', 'mtggoldfish', 'mtggoldfish.com']
    if mtg_source.lower() not in allowed_sources:
        print(f'{mtg_source} is not a supported source')
        exit()
    if mtg_source[-4] == '.':
        mtg_source = mtg_source[:-4]

    mtg_format = args['format']
    allowed_formats = ['modern', 'legacy', 'pioneer']
    if mtg_format.lower() not in allowed_formats:
        print(f'{mtg_format} is not a supported format')
        exit()

    ranking_algo = args['algorithm']
    allowed_algos = ['linear', 'exponential']
    if ranking_algo.lower() not in allowed_algos:
        print(f'{ranking_algo} is not a supported ranking algorithm')
        exit()

    size = int(args['top'])
    if size < 1:
        print(f'{size} must be positive')
        exit()

    date_selection = args['date']

    time_choice = 1

    # Date selection menu if option is provided
    if date_selection:

        time_choice = 0
        while (time_choice < 1) or (time_choice > 4):
            choice = Prompt.ask('Select time range:\n\
        1 Last 2 weeks\n\
        2 Last 2 months\n\
        3 Since beginning of the year\n\
        4 Since specific date\n', choices=['1', '2', '3', '4'])
            try:
                time_choice = int(choice)
                if (time_choice < 1) or (time_choice > 4):
                    print('Invalid choice.')
            except:
                print('Invalid choice.')

    today = datetime.now()
    today_str = today.strftime('%m-%d-%Y')
    today_str_enc = today_str.replace('-', '%2F')

    match time_choice:
        case 1:
            mtgtop8date = '54'
            twoweeksago = today - timedelta(days = 14)
            twoweeksago_str = twoweeksago.strftime('%m-%d-%Y')
            twoweeksago_str_enc = twoweeksago_str.replace('-', '%2F')
            mtggoldfishdate = f'{twoweeksago_str_enc}+-+{today_str_enc}'
            mtgdecks_date = twoweeksago
            time_str = 'over the last 2 weeks'
        case 2:
            mtgtop8date = '51'
            twomonthsago = today - timedelta(days = 60)
            twomonthsago_str = twomonthsago.strftime('%m-%d-%Y')
            twomonthsago_str_enc = twomonthsago_str.replace('-', '%2F')
            mtggoldfishdate = f'{twomonthsago_str_enc}+-+{today_str_enc}'
            mtgdecks_date = twomonthsago
            time_str = 'over the last 2 months'
        case 3:
            mtgtop8date = '246'
            thisyear = today.strftime('%Y')
            beginningoftheyear_str_enc = f'01%2F01%2F{thisyear}'
            mtggoldfishdate = f'{beginningoftheyear_str_enc}+-+{today_str_enc}'
            mtgdecks_date = datetime(today.year, 1, 1)
            time_str = 'since the beginning of the year'
        case 4:
            mtgtop8date = '44'
            date_is_not_valid = True
            while date_is_not_valid:
                specific_date_str = Prompt.ask('Enter date (dd-mm-yyyy):\n')
                try:
                    specific_date = datetime.strptime(specific_date_str, '%d-%m-%Y')
                    if specific_date > today:
                        print('Date must be in the past.')
                    else:
                        date_is_not_valid = False
                except Exception as e:
                    print(e)
                    print('Invalid date format, please use dd-mm-yyyy.')     
            mtgdecks_date = specific_date
            specific_date_str_enc = specific_date.strftime('%m-%d-%Y').replace('-', '%2F')
            mtggoldfishdate = f'{specific_date_str_enc}+-+{today_str_enc}'
            time_str = f'since {specific_date_str}'

    base_url = f'https://mtgtop8.com/format?f={mtg_format[0:2]}&meta={mtgtop8date}&cp='

    match mtg_source:
        case 'mtgdecks':
            base_url = f'https://mtgdecks.net/{mtg_format}/tournaments/page:'
        case 'mtggoldfish':
            base_url = f'https://www.mtggoldfish.com/tournament_searches/create?utf8=%E2%9C%93&tournament_search%5Bname%5D=&tournament_search%5Bformat%5D={mtg_format}&tournament_search%5Bdate_range%5D={mtggoldfishdate}&commit=Search&page='

    decks = crawl_source(base_url, mtg_source, mtg_format, mtgdecks_date, ranking_algo)

    # Printing of results
    print(f'TOP {size} {mtg_format.capitalize()} archetypes {time_str} based on {mtg_source.upper()} and using {ranking_algo} ranking algorithm\n')

    top_decks = sorted(decks.items(), key=lambda x:x[1][0], reverse=True)[0:size]
    for deck in top_decks:
        print(str(top_decks.index(deck)+1)+' - '+deck[0]+' - '+str(deck[1][0])+' pts - '+str(deck[1][1])+' times TOP8')