"""
searchtext=miles+davis+bitches+brew
&currsel=2 # select currency 2
&endfrom=2005 # start year
&endthru=2005 # end year
"""
year = 2003

# RSS SEARCH MARKETPLACE:
# https://www.discogs.com/sell/release/4922985?output=rss
release =  [ 'miles', 'davis', 'sketches', 'of', 'spain' ]
payload = {
            'url': 'https://www.popsike.com/php/quicksearch.php?',
            # here be pseudocode
            'searchtext': {'+'.join(release.to_lower())},
            # ^^^^ PSEUDOCODE FIX ME ^^^^
            'currsel': str(2). # select currency 2 --> canadian dollars
            'endfrom': year, # start year --> endfrom
            'endthru': year # end year ---> endthru (lol)
        }


