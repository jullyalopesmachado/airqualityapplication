from tkinter import *
from PIL import ImageTk, Image
import json

import requests #for API

root = Tk()
root.title("Air quality")
root.geometry("800x300")

my_img = ImageTk.PhotoImage(Image.open("imgs/app.jpg"))

my_Label_img = Label(root, image=my_img)
# Place the label at the top-left corner of the root window
my_Label_img.place(x=0, y=0, relwidth=1, relheight=1)  # x=0, y=0 positions the label at the top-left corner of the window
# relwidth=1 sets the label's width to 100% of the window's width
# relheight=1 sets the label's height to 100% of the window's height
#https://api.api-ninjas.com/v1/quotes?category=happiness

# Create Zip Code function
def ziplookup():
    global weather_color
    try: 
        # Requesting API 
        api_request = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" + zip.get() + "&distance=15&API_KEY=101180E5-E9BC-473D-8A9D-EDBBADEED9AA")
        api = json.loads(api_request.content) # passes the content from API
        city = api[0]['ReportingArea'] # 'ReportingArea' is a section in the API.
        quality = api [0]['AQI'] # This gets the air quality section from the API
        category = api [0]['Category'] ['Name']

        if category == "Good":
            weather_color = "#0C0"
        elif category == "Moderate":
            weather_color = "#FFFF00"
        elif category == "Unhealthy for Sensitive Groups":
            weather_color = "#ff9900"
        elif category == "Unhealthy":
            weather_color = "#FF0000"
        elif category == "Very Unhealthy":
            weather_color = "#990066"
        elif category == "Hazardous":
            weather_color = "#660000"
        
        ## root.configure(background=weather_color)
        myLabel = Label(root, text= city + " Air Quality " + str(quality) + " " + category, font = ("Times", 20, "bold"), background=weather_color) # printing it all in a label. 
        myLabel.grid(row=1, column=0, columnspan=20)
    except Exception as e: # catching errors
        api = "Error"
        
def Quote():
    # Define the category of quotes to fetch
    category = 'happiness'
    
    # Construct the API URL using the category
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    
    # Make a GET request to the API with the specified category
    response = requests.get(api_url, headers={'X-Api-Key': 'hh2yaL4T8I/6o4HdY8435A==L1l1fvU1evCcsVRq'})
    # Fixing the row/column configuration to allow placing quotes in the bottom
    root.grid_rowconfigure(1, weight=1)  # This row will expand and push content to the bottom
    root.grid_rowconfigure(2, weight=0)  # This row will hold the quote_frame
    root.grid_columnconfigure(0, weight=1)
    
    # Create a frame to contain the quote
    quote_frame = Frame(root)  # Optionally set background color
    quote_frame.grid(row=60, column=0, columnspan = 20, rowspan=10)  # Stretch the frame in all directions
    
    # Fixing the row/column configuration to allow placing quotes in the bottom
    quote_frame.grid_columnconfigure(0, weight=1)
    quote_frame.grid_rowconfigure(0, weight=1)
    # Configure row and column weights to allow for centering
    # root.grid_rowconfigure(0, weight=1)
    # root.grid_columnconfigure(0, weight=1)
    
    # Check if the response status code indicates a successful request
    if response.status_code == requests.codes.ok:
        # parse json
        quotes = response.json()
        if quotes:
            quote = quotes[0].get('quote')
            author = quotes[0].get('author')
        # If successful, create a Label widget with the quote text and place it in the Tkinter grid
        my_quote_label = Label(quote_frame, text=quote + " " + "\n " + "By: " + author, font=("Times, 15") ,bg="white", fg="#89CFF0")
        my_quote_label.grid(row=20, column=1)

    else:
        # If the request fails, print the error details to the console
        print("Error:", response.status_code, response.text)
        
        # Define default quote and author values in case of an error (you might want to define 'quote' and 'author' earlier in your code)
        quote = "Error retrieving quote"
        author = "Unknown"
        
       # Create a Label widget with the error message and place it in the Tkinter grid
        new_quote_label = Label(quote_frame, text=quote + " by " + author, background="white")
        new_quote_label.grid(row=0, column=0, padx=1, pady=1)            

zip = Entry(root)
zip.grid(row=0, column=0, sticky=W+E+N+S)

def combined_commands():
    
    ziplookup()
    Quote()
    
zip_Button = Button(root, text="Look up Zipcode",font = ("Times", 15, "bold"), command=combined_commands)
zip_Button.grid(row=0, column=1, sticky=W+E+N+S)

root.mainloop()
