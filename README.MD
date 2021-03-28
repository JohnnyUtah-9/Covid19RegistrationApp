#  Covid19 Vaccine Platform Neutral Registration
   Team Members 
   Kenna King
   Michael Burns 
   Sidney Johnson 
   Tanya Yousofi
- The Vaccine registration app will take user input fields and sort them to multiple organization's online vaccine 
- registration forms and autopopulate their reigstration forms based on state determined priority grouping and geogrpahic promixity
##
# Install Prerequisites:
 - Install Docker on Machine
 - Make sure ports 5000 and 32000 are open
# Install:
- Download Web App Source Code
    - clone https://github.com/drydoesgit/pythonIS601Final
- Start Application
    - docker-compose up
- Docker Build
    - Docker will run Flask App and MySQL DB
- Select Flask App
    - Find 0.0.0:5000
    - *If web app does not run, check firewall settings or try localhost:5000
    
## Instructions
- Enter user input data fields 
- API call routes to connected registration data bases based on selection criteria
