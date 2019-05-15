# travel_info_crawler
This crawler can crawl all travel route information from one travel agency website. 

I use crawl () and parse () to get the url and then parse the url.
 A url containing product information can be obtained through a regular expression while traversing all urls of the entire domain.
 In order to improve speed, I also introduced a Multi-process pool. 

The general execution steps for this crawler: 
Domain Website-> 
All urls in this domain-> 
using RE to get a list of all products pages -> 
Parse all urls in the list -> Get information that contain description and title of a product.
