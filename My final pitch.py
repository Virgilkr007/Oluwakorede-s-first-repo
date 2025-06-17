from tkinter import *
from tkinter import ttk 
from PIL import Image,ImageTk
import webbrowser
import requests
import unicodedata



root= Tk()
root.title("VS pl app")
root.geometry("800x600")
root.minsize(400,300)#Minimal root size a window can go
#root.iconbitmap(r"C:/Users/HP/Desktop/VSLOGO.ico")


def fetch_fixtures_results():
    page2()  # Ensure this function switches to the correct frame

    # Title Label
    Fix_r = Label(Frame2, text="Fixtures & Results", font=("Algerian", 30, "bold", "italic"))
    Fix_r.place(relx=0.3, rely=0.01)

    def get_team_names():
        """Fetches team names from the API and returns a dictionary mapping team IDs to names."""
        response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/", timeout=15)
        if response.status_code == 200:
            teams_data = response.json().get("teams", [])
            return {team["id"]: team["name"] for team in teams_data}
        return {}

    def fetch_fixtures():
        """Fetches Premier League fixtures and results from the API."""
        response = requests.get("https://fantasy.premierleague.com/api/fixtures/", timeout=15)
        return response.json() if response.status_code == 200 else []

    def update_fixtures():
        """Updates the fixtures/results table with new data."""
        fixtures = fetch_fixtures()
        if not fixtures:
            status_label.config(text="Failed to load fixtures. Try again.")
            return

        tree.delete(*tree.get_children())  # Clear previous data

        for fixture in fixtures:
            home_team = team_names.get(fixture["team_h"], "Unknown")
            away_team = team_names.get(fixture["team_a"], "Unknown")
            gameweek = fixture["event"]

            # Check if the match has been played (scores available)
            score = f"{fixture['team_h_score']} - {fixture['team_a_score']}" if fixture.get("team_h_score") is not None else "Upcoming"

            tree.insert("", "end", values=(gameweek, home_team, score, away_team))

        status_label.config(text="Fixtures updated successfully!")

    # Fetch team names before loading fixtures
    team_names = get_team_names()

    # Table to display fixtures
    tree = ttk.Treeview(Frame2, columns=("Gameweek", "Home Team", "Score", "Away Team"), show="headings", height=15)
    tree.heading("Gameweek", text="GW")
    tree.heading("Home Team", text="Home")
    tree.heading("Score", text="Score")
    tree.heading("Away Team", text="Away")

    tree.column("Gameweek", width=60, anchor="center")
    tree.column("Home Team", width=180, anchor="center")
    tree.column("Score", width=80, anchor="center")
    tree.column("Away Team", width=180, anchor="center")

    tree.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.6)  # Positioned within the frame

    # Refresh Button
    refresh_btn = Button(Frame2, text="Refresh Fixtures", command=update_fixtures)
    refresh_btn.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.08)

    # Status Label
    status_label = Label(Frame2, text="", font=("Arial", 10))
    status_label.place(relx=0.3, rely=0.85, relwidth=0.4)

    # Initial Load
    update_fixtures()








def player_details():
    page5()
    Player_Label = Label(Frame5, text="Players", font=("Algerian", 30, "bold"), fg="Purple")
    Player_Label.place(relx=0.4, rely=0.01)

    url = "https://fantasy.premierleague.com/api/bootstrap-static/"

    def fetch_data():
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            players = data.get("elements", [])

            # Debugging: Print all player names to confirm data exists
            print("Checking players in API data:")
            for player in players:
                print(f"{player['first_name']} {player['second_name']}")

            return players
        else:
            status_label.config(text=f"{response.status_code} - Failed to fetch data")
            return None

    players = fetch_data()
    positions = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Forward"}

    def normalize_name(name):
        """Remove accents and normalize names for better searching."""
        return unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')

    def search_player():
        if not players:
            status_label.config(text="No data available. Try refreshing.")
            return

        name = normalize_name(entry.get().strip().lower())  # Normalize user input
        best_match = None  

        for player in players:
            full_name = f"{player['first_name']} {player['second_name']}"
            full_name_normalized = normalize_name(full_name.lower())  # Normalize stored names
            team= player["team"]


            if name in full_name_normalized:  # Allows "nunez" to match "núñez"
                best_match = player
                break  

        if best_match:
            name_label.config(text=f"Name: {best_match['first_name']} {best_match['second_name']}")
            pos_label.config(text=f"Position: {positions.get(best_match['element_type'], 'Unknown')}")
            nation_label.config(text=f"Nationality: {best_match.get('nationality', 'Unknown')}")
            points_label.config(text=f"Total Points: {best_match.get('total_points', 'N/A')}")
            team_label.config(text=f"Team: {team.get("team","Unknown")}")

        else:
            name_label.config(text="Player not found!")
            pos_label.config(text="Position: N/A")
            nation_label.config(text="Nationality: N/A")
            points_label.config(text="Total Points: N/A")
            team_label.config(text="Club:N/A")

    def refresh_data():
        nonlocal players  # Ensure we update the existing players list
        players = fetch_data()
        status_label.config(text="Data refreshed successfully!" if players else "Failed to refresh data.")

    entry = Entry(Frame5, width=30, borderwidth=10)
    entry.place(relx=0.1, rely=0.1)
    
    search_btn = Button(Frame5, text="Search", command=search_player)
    search_btn.place(relx=0.05, rely=0.1)

    name_label = Label(Frame5, text="Name: ", font=("Arial", 12))
    name_label.place(relx=0.1, rely=0.2)
    
    pos_label = Label(Frame5, text="Position: ", font=("Arial", 12))
    pos_label.place(relx=0.1, rely=0.3)
    
    nation_label = Label(Frame5, text="Nationality: ", font=("Arial", 12))
    nation_label.place(relx=0.1, rely=0.4)
    
    points_label = Label(Frame5, text="Total Points: ", font=("Arial", 12))
    points_label.place(relx=0.1, rely=0.5)

    Team_label = Label(Frame5, text="Club: ", font=("Arial", 12))
    Team_label.place(relx=0.1, rely=0.6)

    refresh_btn = Button(Frame5, text="Refresh Data", command=refresh_data)
    refresh_btn.place(relx=0.5, rely=0.95)

    # Status label
    status_label = Label(Frame5, text="", font=("Arial", 10))
    status_label.pack()

    # Auto-refresh every 5 minutes
    root.after(300000, refresh_data)
    
#Teams = ("Liverpool", "Arsenal", "Chelsea", "Manchester united", "Manchester city", "Tottenham", "Fullham", "Nottingham Forest", "Brighton", "Brentford", "Wolverhampton wanderers", "Leicester city", "Ipswich Town", "Southampton", "Westham United", "Everton", "Crystal Palace", "Newcastle", "Bournemouth", "Aston Villa")   
def premier_league_table():
    page3()
    Table= [
        {"team":"Liverpool","Matches Played":22,"Wins":16,"Draws":5,"Losses":1,"Points":53},
        {"team":"Arsenal","Matches Played":23,"Wins":13,"Draws":8,"Losses":2,"Points":47},
        {"team":"Chelsea","Matches Played":23,"Wins":11,"Draws":7,"Losses":5,"Points":40},
        {"team":"Manchester united","Matches Played":23,"Wins":8,"Draws":5,"Losses":10,"Points":29},
        {"team":"Manchester city","Matches Played":23,"Wins":12,"Draws":5,"Losses":6,"Points":41},
        {"team":"Tottenham","Matches Played":23,"Wins":7,"Draws":3,"Losses":13,"Points":24},
        {"team":"Fullham","Matches Played":23,"Wins":8,"Draws":9,"Losses":6,"Points":33},
        {"team":"Nottingham Forest","Matches Played":23,"Wins":13,"Draws":5,"Losses":5,"Points":44},
        {"team":"Brighton","Matches Played":23,"Wins":8,"Draws":10,"Losses":5,"Points":34},
        {"team":"Brentford","Matches Played":23,"Wins":9,"Draws":4,"Losses":10,"Points":31},
        {"team":"Wolverhampton wanderers","Matches Played":23,"Wins":4,"Draws":4,"Losses":15,"Points":16},
        {"team":"Leicester city","Matches Played":23,"Wins":4,"Draws":5,"Losses":14,"Points":17},
        {"team":"Ipswich Town","Matches Played":23,"Wins":3,"Draws":7,"Losses":13,"Points":16},
        {"team":"Southampton","Matches Played":23,"Wins":1,"Draws":3,"Losses":19,"Points":6},
        {"team":"Westham United","Matches Played":23,"Wins":7,"Draws":6,"Losses":10,"Points":27},
        {"team":"Everton","Matches Played":22,"Wins":5,"Draws":8,"Losses":9,"Points":23},
        {"team":"Crystal Palace","Matches Played":23,"Wins":6,"Draws":9,"Losses":8,"Points":27},
        {"team":"Newcastle","Matches Played":23,"Wins":12,"Draws":5,"Losses":6,"Points":41},
        {"team":"Bournemouth","Matches Played":23,"Wins":11,"Draws":7,"Losses":5,"Points":40},
        {"team":"Aston Villa","Matches Played":23,"Wins":10,"Draws":7,"Losses":6,"Points":37}
        ]

    # Treeview Table
    Prem_Table = ttk.Treeview(Frame3, columns=("team", "Matches Played", "Wins", "Draws", "Losses", "Points"), show="headings")

    # Defining the headings
    column_names = ["Clubs", "MP", "W", "D", "L", "Pts"]
    table_keys = ["team", "Matches Played", "Wins", "Draws", "Losses", "Points"]

    for col, key in zip(column_names, table_keys):
        Prem_Table.heading(key, text=col)
        Prem_Table.column(key, width=100 if key == "team" else 50)

    # Insert Data
    for logs in Table:
        Prem_Table.insert("", "end", values=tuple(logs.values()))

    Prem_Table.pack(fill="both", expand=True, pady=10)

    # Dropdown Menu for Selecting Team
    selected_team = StringVar()
    selected_team.set(Table[0]["team"])  # Default selection

    team_dropdown = OptionMenu(Frame3, selected_team, *[team["team"] for team in Table])
    team_dropdown.place(relx=0.1, rely=0.85)

    # Entry Fields for Updating Stats
    entries = {}
    fields = ["Matches Played", "Wins", "Draws", "Points"]

    for i, field in enumerate(fields):
        Label(Frame3, text=field).place(relx=0.3 + i * 0.15, rely=0.8)  # Labels
        entry = Entry(Frame3, width=5)
        entry.place(relx=0.3 + i * 0.15, rely=0.85)  # Entries
        entries[field] = entry

    # Auto-calculated Losses Label
    losses_label = Label(Frame3, text="Losses: 0")
    losses_label.place(relx=0.9, rely=0.85)

    # Function to Update the Table
    def update_table():
        team_name = selected_team.get()
        updated_values = {}

        for field, entry in entries.items():
            try:
                updated_values[field] = int(entry.get())  # Convert input to int
            except ValueError:
                updated_values[field] = None  # Handle invalid input

        # Auto-calculate losses
        if all(updated_values.get(key) is not None for key in ["Matches Played", "Wins", "Draws"]):
            updated_values["Losses"] = updated_values["Matches Played"] - (updated_values["Wins"] + updated_values["Draws"])
            losses_label.config(text=f"Losses: {updated_values['Losses']}")

        # Update Data
        for team in Table:
            if team["team"] == team_name:
                for key, value in updated_values.items():
                    if value is not None:
                        team[key] = value

        # Clear Table and Reinsert Updated Data
        for row in Prem_Table.get_children():
            Prem_Table.delete(row)

        for logs in Table:
            Prem_Table.insert("", "end", values=tuple(logs.values()))

    # Update Button
    update_button = Button(Frame3, text="Update", command=update_table)
    update_button.place(relx=0.5, rely=0.9)  # Centered below entries




def statistics():
    page4()
    Players_with_highest_number_of_goals = [
        ("Mohammed Salah", "Liverpool", 17),
        ("Luis Diaz", "Liverpool", 8),
        ("Erling Haaland", "Man City", 14),
        ("Cole Palmer", "Chelsea", 12), 
        ("Chris Wood", "Nottingham Forest", 11),
        ("Alexander Isak", "Newcastle", 12),
        ("Matheus Cunha", "Wolverhampton Wanderers", 10),
        ("Bryan Mbeumo", "Brentford", 10),
        ("Yoane Wissa", "Brentford", 9),
        ("Nicolas Jackson", "Chelsea", 9)
        ]

    Players_with_highest_assists = [
        ("Mohammed Salah", "Liverpool", 13),
        ("Bukayo Saka", "Arsenal", 10),
        ("Cole Palmer", "Chelsea", 6),
        ("Jarod Bowen", "Westham", 5),
        ("Joao Pedro", "Brighton", 5),
        ("Bruno Fernandes", "Manchester United", 5),
        ("Heung-min Son", "Tottenham", 6),
        ("Antonee Robinson", "Fulham", 7),
        ("Jacob Murphy", "Newcastle", 6),
        ("Amad Diallo", "Manchester United", 5)
        ]
    
    
    Players_with_highest_number_of_yellow_cards = [
        ("Will Hughes", "Crystal Palace", 7),
        ("Marc Cucrella", "Chelsea", 7),
        ("Boubakary Soumare", "Leicester City", 7),
        ("Wesley Fofana", "Chelsea", 6),
        ("Sasa Lukic", "Fulham", 7),
        ("Flynn Downes", "Southampton", 7),
        ("Joao Gomes", "Wolverhampton Wanderers", 6),
        ("Liam Delap", "Ipswich Town", 6),
        ("Joelinton", "Newcastle", 6),
        ("Lisandro Martinez", "Manchester United", 6)
        ]
    
    Players_highest_number_of_red_cards = [
        ("Jack Stephens", "Southampton", 2),
        ("Mohammed Kudus", "Westham United", 1),
        ("Andy Robertson", "Liverpool", 1),
        ("Bruno Fernandes", "Manchester United", 2),
        ("William Saliba", "Arsenal", 1),
        ("Ashley Young", "Everton", 1),
        ("Christian Norgaard", "Brentford", 1),
        ("Fabian Schar", "Newcastle", 1),
        ("Ryan Fraser", "Southampton", 1),
        ("Jhon Duran", "Aston Villa", 1)
        ]
    
    # Functions to update player stats
    def update_stats(player_list, player_name, statictic, new_value):
        for index, (name, team, stat) in enumerate(player_list):
            if name == player_name:
                player_list[index] = (name, team, new_value)
                return True
            else:
                return False
    
    # Function to display the selected statistic table
    def display_stats(statistic):
        # Clear previous content
        for widget in stats_frame.winfo_children():
            widget.destroy()
            
        # Select the correct data based on the stat type
        if statistic == "Goals":
            players = Players_with_highest_number_of_goals
            header = ["Position", "Name", "Team", "Goals"]
        elif statistic == "Assists":
            players = Players_with_highest_assists
            header = ["Position", "Name", "Team", "Assists"]
        elif statistic == "Yellow Cards":
            players = Players_with_highest_number_of_yellow_cards
            header = ["Position", "Name", "Team", "Yellow Cards"]
        elif statistic == "Red Cards":
            players = Players_highest_number_of_red_cards
            header = ["Position", "Name", "Team", "Red Cards"]
            print ("_" * 72)
            
        # Sort the players by the statistic (descending)
        players = sorted(players, key=lambda x: x[2], reverse=True)
        
        for col, header in enumerate(header):
            label= Label(stats_frame, text=header, width=20, font=("Arial", 10, "bold"))
            label.grid(row=0, column=col)
        
        # Display the players' stats
        for row, (name, team, stat) in enumerate(players, start=1):
            Label(stats_frame, text=f"{row}", width=10).grid(row=row, column=0)
            Label(stats_frame, text=name, width=40).grid(row=row, column=1)
            Label(stats_frame, text=team, width=40).grid(row=row, column=2)
            Label(stats_frame, text=stat, width=40).grid(row=row, column=3)
    
    # Function to handle updating the stats
    def submit_update():
        player_name = player_name_entry.get()
        new_value = int(new_value_entry.get())
        stat_type = stat_var.get()
        
        if stat_type == "Goals":
            updated = update_stats(Players_with_highest_number_of_goals, player_name, stat_type, new_value)
        elif stat_type == "Assists":
            updated = update_stats(Players_with_highest_assists, player_name, stat_type, new_value)
        elif stat_type == "Yellow Cards":
            updated = update_stats(Players_with_highest_number_of_yellow_cards, player_name, stat_type, new_value)
        elif stat_type == "Red Cards":
            updated = update_stats(Players_highest_number_of_red_cards, player_name, stat_type, new_value)
            
        if updated:
            messagebox.showinfo("Success", f"Updated {stat_type} for {player_name}!")
            display_stats(stat_type)
        else:
            messagebox.showerror("Error", "Player not FOUND")
            
    # Dropdown menu for selecting stats category
    stat_var = StringVar()
    stat_var.set("Goals") # Default value
    
    stat_menu = OptionMenu(Frame4,stat_var, "Goals", "Assists", "Yellow Cards", "Red Cards", command=display_stats)
    stat_menu.pack(pady=10)
    
    # Frame for displaying stats tables
    stats_frame = Frame(Frame4)
    stats_frame.pack()
    
    # Inputs for updating stats
    update_frame = Frame(Frame4)
    update_frame.pack(pady=20)
    
    Label(update_frame, text="Player Name:").grid(row=0, column=0)
    player_name_entry = Entry(update_frame)
    player_name_entry.grid(row=0, column=1)
    
    Label(update_frame, text="New Value:").grid(row=1, column=0)
    new_value_entry = Entry(update_frame)
    new_value_entry.grid(row=1, column=1)
    
    update_button = Button(update_frame, text="Update Stats", command=submit_update)
    update_button.grid(row=2, columnspan=2, pady=10)
    
    display_stats("Goals")

#Frame for the home page 
def page1():
    Frame2.pack_forget()
    Frame3.pack_forget()
    Frame4.pack_forget()
    Frame5.pack_forget()
    Frame6.pack_forget()
    Frame1.pack(fill="both", expand=True)    



#Frame for Matches
def page2():
    Frame3.pack_forget()
    Frame4.pack_forget()
    Frame5.pack_forget()
    Frame6.pack_forget()
    Frame1.pack_forget()
    Frame2.pack(fill="both", expand=True)

#Frame for Table
def page3():
    Frame2.pack_forget()
    Frame1.pack_forget()
    Frame4.pack_forget()
    Frame5.pack_forget()
    Frame6.pack_forget()
    Frame3.pack(fill="both", expand= True)


#Frame for Statistics
def page4():
    Frame1.pack_forget()
    Frame2.pack_forget()
    Frame3.pack_forget()
    Frame5.pack_forget()
    Frame6.pack_forget()
    Frame4.pack(fill="both", expand=True)

#Frame for Players
def page5():
    Frame1.pack_forget()
    Frame2.pack_forget()
    Frame3.pack_forget()
    Frame4.pack_forget()
    Frame6.pack_forget()
    Frame5.pack(fill="both", expand=True)

#Frame for watch
def page6():
    Frame1.pack_forget()
    Frame2.pack_forget()
    Frame3.pack_forget()
    Frame4.pack_forget()
    Frame5.pack_forget()
    Frame6.pack(fill="both", expand=True)

#Making each frame a root
Frame1= Frame(root)
Frame2= Frame(root)
Frame3= Frame(root)
Frame4= Frame(root)
Frame5= Frame(root)
Frame6= Frame(root)


def links():
    Click= Label(Frame6, text= "Click any of the links below", font= ("Times New Roman",40,"bold"),fg = "Purple" )
    Link_1= Label(Frame6, text= "https://afr.score808.tv/football.html", fg= "light blue", cursor= "hand2" )
    Link_2= Label(Frame6, text= "https://www.tosinaija.com/", fg= "light blue", cursor= "hand2")
    Link_3= Label(Frame6, text= "https://fullmatchsports.cc/full-match-replay/page/3/", fg= "light blue", cursor= "hand2")
    Link_4= Label(Frame6, text= "https://www.hesgoal.watch/", fg= "light blue", cursor= "hand2")

     
    Click.place(relx=0.2,rely= 0.1)
    Link_1.place(relx= 0.3, rely= 0.3)
    Link_2.place(relx=0.3,rely=0.4)
    Link_3.place(relx= 0.3, rely=0.5)
    Link_4.place(relx=0.3, rely=0.6)
    
    Link_1.bind("<Button-1>", lambda e: webbrowser.open("https://afr.score808.tv/football.html"))
    Link_2.bind("<Button-1>", lambda e: webbrowser.open("https://www.tosinaija.com/"))
    Link_3.bind("<Button-1>", lambda e: webbrowser.open("https://fullmatchsports.cc/full-match-replay/page/3/"))
    Link_4.bind("<Button-1>", lambda e: webbrowser.open("https://www.hesgoal.watch/"))


def watch():
    page6()
    links()



    
    
Backward_button= Button(root, text="Home page",width= 10, pady=4, padx=10, fg= "white", bg="Light green", font=("Canva sans", 12, "bold","italic" ), command= page1)

Matches_button= Button(Frame1, text= "Matches",width =50 ,padx=50, pady=20, font= ("Open Sans", 10, "bold"), bg= "Navy Blue", fg = "White",cursor="hand2",command=fetch_fixtures_results)
Table_button= Button(Frame1, text= "Table",width=50, padx= 50, pady=20, font= ("Open Sans", 10, "bold"), bg= "Navy Blue", fg = "White",cursor="hand2",command=premier_league_table)
Players_button= Button(Frame1, text= "Players",width=50, padx= 50, pady=20, font= ("Open Sans", 10, "bold"), bg= "Navy Blue", fg = "White",cursor="hand2", command=player_details)
Statistics_button= Button(Frame1, text= "Statistics",width=50, padx= 50, pady=20, font= ("Open Sans", 10, "bold"), bg= "Navy Blue", fg = "White",cursor="hand2",command=statistics)
Watch_button= Button(Frame1, text= "Watch live",width=50, padx=50, pady=20, font= ("Open Sans", 10, "bold"), bg= "Navy Blue", fg = "White",cursor="hand2", command= watch)

Matches_button.place(relx=0.5,rely=0.3, anchor="center")
Table_button.place(relx=0.5,rely=0.4, anchor="center")
Statistics_button.place(relx=0.5,rely=0.5, anchor="center")
Players_button.place(relx=0.5,rely=0.6, anchor="center")
Watch_button.place(relx=0.5,rely=0.7, anchor="center")

Backward_button.place(relx=0.0, rely=0.95)

#Note: You can not use pack and grid in the same frame, but place can be used with either of them because it is independent of them

Frame1.pack(fill="both", expand= True)
Frame1.update_idletasks()



root.mainloop()