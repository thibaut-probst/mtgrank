from argparse import ArgumentParser, RawTextHelpFormatter
from rich.prompt import Prompt
from rich.progress import Progress
from datetime import datetime, timedelta
from requests import get
from bs4 import BeautifulSoup
from re import compile

mtgtop8_base_url = 'https://mtgtop8.com'
user_agent = {'User-agent': 'Mozilla/5.0'}

def select_format():
    '''
    Parses the website data source website to identify the available Magic: The Gathering formats and prompts the user to select a format.

    Returns:
        The selected Magic: The Gathering format.
    '''

    # Format discovery
    format_choice_str = 'Select a format:\n'
    mtg_formats = {}
    response = get(f'{mtgtop8_base_url}', headers=user_agent)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    n = 1
    for link in links:
        href = link.get('href')
        if href:
            if href.startswith('/format?f='):
                mtg_formats[n] = href.split('=')[1]
                if link.text.lower() == 'cedh':
                    format_choice_str += f'{n} - cEDH\n'
                else:
                    format_choice_str += f'{n} - {link.text.title()}\n'
                n += 1
    # Format choice
    format_choice = 0
    while format_choice == 0:
        format_choice = Prompt.ask(format_choice_str, choices=[f'{n}' for n in mtg_formats.keys()], show_choices=False)
        try:
            format_choice = int(format_choice)
            if format_choice == 0:
                print('Invalid choice.')
        except Exception:
            print('Invalid choice.')

    return mtg_formats[format_choice]

def crawl_event(url, mtg_format, algo):
    '''
    MTG event crawling function
        
            Parameters:
                url (str): event url
                mtg_format (str): MTG format
                algo (str): ranking algorithm
            Returns:
                deck_ranking (dict): event deck ranking
    ''' 

    deck_ranking = {}

    # Send an HTTP GET request to the URL
    response = get(url, headers = user_agent)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Process the HTML content
        links_in_event = soup.find_all('a')

        # Look for the number of players in the tournament, if not found set it to 8
        nb_players = 8

        nb_players_regex = compile('([0-9]+) players')

        try:
            nb_players = int(nb_players_regex.findall(response.text)[0])
        except Exception:
            pass

        decks = []
        for link in links_in_event:
            # Find all the links on the page
            href = link.get('href')
            txt = link.text
            if href and txt:
                href = href.lower()
                # Only keep decks
                if (len(txt) > 1) and ('Winrates' not in txt):
                    if (href.startswith('?e=') and ( (href.endswith(f'&f={mtg_format.lower()[0:2]}')) or (href.endswith(f'&f={mtg_format.lower()[0:3]}')) or (href.endswith(f'&f={mtg_format.lower()[0:4]}'))) ) or\
                        (href.startswith(f'/{mtg_format}/') and (not href.startswith(f'/{mtg_format}/tournaments')) and (not href.startswith(f'/{mtg_format}/staples')) and (not href.startswith('/{mtg_format}/winrates'))) or\
                        (href.startswith('/deck/') and (not href.startswith('/deck/custom/')) and (not href.startswith('/deck/visual/'))):
                        response = get(f'{mtgtop8_base_url}/event{href}', headers = user_agent)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            links_in_deck = soup.find_all('a')
                            for link_in_deck in links_in_deck:
                                d_href = link_in_deck.get('href')
                                if d_href:
                                    if 'archetype?a=' in d_href:
                                        archetype = link_in_deck.text.split(' decks')[0]
                                        decks.append(archetype)                        
                            
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


def crawl_source(url, mtg_format, date, paper_online_or_both, algo):
    '''
    MTG source crawling function
        
            Parameters:
                url (str): event url
                mtg_format (str): MTG format
                date (datetime.date): date to look up to
                paper_online_or_both (str): type of events to analyze (paper, online or both)
                algo (str): ranking algorithm
            Returns:
                global_deck_ranking (dict): global deck ranking
    '''

    global_deck_ranking = {}
    user_agent = {'User-agent': 'Mozilla/5.0'}
    
    p = 1

    with Progress() as progress:
        task = progress.add_task('Parsing MTGTOP8...', total=100, visible=True)

        today = datetime.now()
        previous_date = today
        total_period = today - date

        # Loop until we hit a page with no more event links or the date is passed
        while True:

            # Send an HTTP GET request to the URL
            response = get(f'{url}{p}', headers = user_agent)
            
            # Check if the request was successful
            if response.status_code == 200:
                
                # Parse the HTML content
                resp = response.text
                body = resp
                try:
                    body = resp.split('LAST 20 EVENTS')[1]
                except Exception:
                    try:
                        body = resp.split('align=center>Events ')[1]
                    except Exception:
                        exit()
                
                soup = BeautifulSoup(body, 'html.parser')

                # Estimate progress
                events_before_date = []

                # Check event dates

                # Specific date provided, check event dates but also not to parse events over time range
                event_before_date = False
                if '&meta=44' in url:
                    event_dates = compile('[0-9]+/[0-9]+/[0-9]+').findall(body) # Dates are within strong HTML elements
                    oldest_event_date = None
                    for event_date_raw in event_dates: 
                        event_date = datetime.strptime(event_date_raw, '%d/%m/%y')
                        if event_date < date:
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
                
                # Find all the links on the page to look for events
                links = soup.find_all('a')
                events = []

                for link in links:
                    href = link.get('href')

                    if href:
                        href = href.lower()
                        # Only keep event links
                        if (href.startswith('event?e=') and (href.endswith(f'={mtg_format.lower()[0:2]}') or href.endswith(f'={mtg_format.lower()[0:3]}') or href.endswith(f'={mtg_format.lower()[0:4]}')) and ((link.text not in events_before_date))):
                            if (paper_online_or_both == 'paper') and (not link.text.startswith('MTGO')):
                                events.append(href)
                            elif (paper_online_or_both == 'online') and (link.text.startswith('MTGO')):
                                events.append(href)
                            elif (paper_online_or_both == 'both'):
                                events.append(href)

                deck_ranking_event = {}
                events = list(set(events)) # Avoid duplicates

                # Crawl events
                for event in events:
                    deck_ranking_event = crawl_event(f'{mtgtop8_base_url}/{event}', mtg_format, algo)

                    for deck in deck_ranking_event.keys():
                        pts = deck_ranking_event[deck][0]
                        timestop8 = deck_ranking_event[deck][1]
                        if deck not in global_deck_ranking.keys():
                            global_deck_ranking[deck] = [pts, timestop8]
                        else:
                            global_deck_ranking[deck] = [global_deck_ranking[deck][0]+pts, global_deck_ranking[deck][1]+timestop8]
                
                    progress.update(task, advance=period_progress / len(events))

                # Check if no more events
                if ((('<div class=Nav_PN_no>Next</div>' in body) or event_before_date )):
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
        '--format', '-f',
        type = str,
        action = 'store',
        default = '',
        help = 'The format to analyze (default: interactive mode)'
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

    paper_online = parser.add_mutually_exclusive_group()

    paper_online.add_argument(
        '--paper', '-p',
        action = 'store_true',
        help = 'Only analyze paper events'
    )
    
    paper_online.add_argument(
        '--online', '-o',
        action = 'store_true',
        help = 'Only analyze online events'
    )

    args = vars(parser.parse_args())

    ranking_algo = args['algorithm']
    allowed_algos = ['linear', 'exponential']
    if ranking_algo.lower() not in allowed_algos:
        print(f'{ranking_algo} is not a supported ranking algorithm')
        exit()

    size = int(args['top'])
    if size < 1:
        print(f'{size} must be positive')
        exit()

    input_format = args['format']
    mtg_format = input_format.upper()
    allowed_formats = ['ST', 'STD', 'STANDARD', 'PI', 'PIONEER', 'MO', 'MODERN', 'LE', 'LEGACY', 'VI', 'VINTAGE', \
                       'PAU', 'PAUPER', 'cEDH', 'COMMANDER', 'DC', 'EDH', 'DUELCOMMANDER', 'DUEL COMMANDER', 'PREM', 'PREMODERN']
    if mtg_format:
        if mtg_format not in allowed_formats:
            print(f'{input_format} is not in the list of supported formats.')
            exit()
        else:
            if (mtg_format == 'PAUPER'):
                mtg_format = 'PAU'
            elif (mtg_format == 'COMMANDER'):
                mtg_format = 'cEDH'
            elif (mtg_format == 'DC') or (mtg_format == 'EDH') or mtg_format.startswith('DUEL'):
                mtg_format = 'EDH'
            elif (mtg_format == 'PREMODERN'):
                mtg_format = 'PREM'
            else:
                mtg_format = mtg_format[0:2]

    paper = args['paper']
    online = args['online']
    paper_online_or_both = 'both'
    paper_online_both_str = 'both paper and online events'
    if paper:
        paper_online_or_both = 'paper'
        paper_online_both_str = 'paper only events'
    elif online:
        paper_online_or_both = 'online'
        paper_online_both_str = 'online only events'

    if not mtg_format:
        mtg_format = select_format()

    date_selection = args['date']

    time_choice = 1

    # Date selection menu if option is provided
    if date_selection:

        time_choice = 0
        while (time_choice < 1) or (time_choice > 4):
            choice = Prompt.ask('Select time range:\n\
        1 Last 2 weeks\n\
        2 Last 2 months\n\
        3 Since the beginning of the year\n\
        4 Since a specific date\n', choices=['1', '2', '3', '4'])
            try:
                time_choice = int(choice)
                if (time_choice < 1) or (time_choice > 4):
                    print('Invalid choice.')
            except Exception:  # noqa: E722
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
            specific_date = twoweeksago
            time_str = 'over the last 2 weeks'
        case 2:
            mtgtop8date = '51'
            twomonthsago = today - timedelta(days = 60)
            twomonthsago_str = twomonthsago.strftime('%m-%d-%Y')
            twomonthsago_str_enc = twomonthsago_str.replace('-', '%2F')
            specific_date = twomonthsago
            time_str = 'over the last 2 months'
        case 3:
            mtgtop8date = '246'
            thisyear = today.strftime('%Y')
            beginningoftheyear_str_enc = f'01%2F01%2F{thisyear}'
            specific_date = datetime(today.year, 1, 1)
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
            specific_date_str_enc = specific_date.strftime('%m-%d-%Y').replace('-', '%2F')
            time_str = f'since {specific_date_str}'

    base_url = f'{mtgtop8_base_url}/format?f={mtg_format}&meta={mtgtop8date}&cp='

    decks = crawl_source(base_url, mtg_format, specific_date, paper_online_or_both, ranking_algo)

    # Printing of results
    if mtg_format == 'EDH':
        mtg_format = mtg_format.upper()
    elif mtg_format == 'cEDH':
        pass
    else:
        mtg_format = mtg_format.title()
    print(f'TOP {size} {mtg_format} archetypes {time_str} based on MTGTOP8 for {paper_online_both_str} and using {ranking_algo} ranking algorithm\n')

    top_decks = sorted(decks.items(), key=lambda x:x[1][0], reverse=True)[0:size]
    for deck in top_decks:
        print(str(top_decks.index(deck)+1)+' - '+deck[0]+' - '+str(deck[1][0])+' pts - '+str(deck[1][1])+' times TOP8')