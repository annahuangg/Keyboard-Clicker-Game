import tkinter as tk
import unicodedata
from pathlib import Path

key_symb = '\U000026bf'
bg_color = "turquoise"

class KeyClick(tk.Tk):
 
    def __init__(self, *args, **kwargs):
        
        '''This function, __init__, within the object, KeyClick, sets the main 
        parameters for the entire program and allows a way to switch between frames'''
        
        tk.Tk.__init__(self, *args, **kwargs)
        main_frame = tk.Frame(self)
        
        main_frame.pack(side="top", fill="both", expand = True)
        
        self.frames = {}
        
        for page in (Main_menu, Rules, Save_Frame, Game, Starting_frame, Upgrades):
            frame = page(main_frame, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(Starting_frame)
        self.after(1000, lambda: self.show_frame(Main_menu))
    
    def show_frame(self, cont):
        
        '''This function, show_frame, within the object, KeyClick, will display 
        the frame of whatever frame is used as it's parameter. This also allows
        displays the saved counter in the event that the user clicks resume'''
        
        frame = self.frames[cont]
        if Game == cont:
            displaySavedCounter()
        frame.tkraise()
    
###############################################################################

class Upgrades(tk.Frame):
    
    def __init__(self, parent, controller):
        
        '''This function, __y_n__, will give the option to upgrade their key-clicking capacity for the price of keys.'''
        
        global click_Upgrade_list
        
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg=bg_color)
        
        time_label = tk.Label(self, text="Time Upgrade", font="LARGE_FONT",bg = bg_color)

        time_label.pack(padx=5, pady=25)
        
        if len(time_Upgrade_list) == 0:
            Time_Upgrade_button = tk.Label(self, text="No More Upgrades Available", 
                                            bg="black", fg="white")
            Time_Upgrade_button.pack(padx=5, pady=25)
        else:
            Upgrades.Time_Upgrade_button = tk.Button(self, text="Upgrade: "+str(time_Upgrade_list[0][1])+" Keys per Second\nCost: "+str(time_Upgrade_list[0][0])+" Keys", 
                                                         bg="black",
                                                         fg="white",
                                                         command=time_upgrade_menu)
            Upgrades.Time_Upgrade_button.pack(padx=5, pady=25)
    
        click_label = tk.Label(self, text="Click Upgrade", font="LARGE_FONT",bg = bg_color)

        click_label.pack(padx=5, pady=25)
        
        if len(click_Upgrade_list) == 0:
            Click_Upgrade_button = tk.Label(self, text="No More Upgrades Available",
                                             bg="black", fg="white")
                                     
            Click_Upgrade_button.pack(padx=5, pady=25)
        else:
            Upgrades.Click_Upgrade_button = tk.Button(self, text="Upgrade: "+str(click_Upgrade_list[0][1])+" Keys per Click\nCost: "+str(click_Upgrade_list[0][0])+" Keys",
                                             bg="black", fg="white",
                                             command=click_upgrade)
                                     
            Upgrades.Click_Upgrade_button.pack(padx=5, pady=25)
        
        Back_button = tk.Button(self, text="Back", bg= "black", fg="white",
                                font="LARGE_FONT",
                                command= lambda: controller.show_frame(Game))
        Back_button.pack(side=tk.RIGHT, padx=10, pady=20)
        
#####################################################################

click_Upgrade_list = [[100, 2], [1000, 3], [50000, 10], [100000, 35], [5000000, 50], [1000000000, 125]]
time_Upgrade_list = [[100, 1], [1000, 2], [50000, 4], [100000, 9], [5000000, 25], [1000000000, 75]]
count = 0
count_num = 1
keys_per_sec = 0
click_upgrade_count = 0
time_upgrade_count = 0
first_resume = True
running_auto_key = True
first_auto_key = True

def click_upgrade():
    global count
    global count_num
    global click_Upgrade_list
    global click_upgrade_count
    
    click_Upgrade_list = click_Upgrade_list
    if count < click_Upgrade_list[0][0]:
        tk.messagebox.showinfo(title="Information", message="Not enough keys")

    else:
        count = count - click_Upgrade_list[0][0]
        count_num = click_Upgrade_list[0][1]
        click_upgrade_count += 1
    
        click_Upgrade_list.remove(click_Upgrade_list[0])
        Upgrades.Click_Upgrade_button.config(text="Upgrade: "+str(click_Upgrade_list[0][1])+" Keys per Click\nCost: "+str(click_Upgrade_list[0][0])+" Keys")
        KeyboardClicker.show_frame(Game)

###############################################################################

def time_upgrade_menu():
    global count
    global time_Upgrade_list
    global time_upgrade_count
    global keys_per_sec
    global first_auto_key
    time_Upgrade_list = time_Upgrade_list

    def auto_key():
        global count
        global keys_per_sec
        global running_auto_key
        if running_auto_key == True:
            count += keys_per_sec
            Game.key_label.config(text="You have "+str(count)+" "+key_symb+"'s")
            Game.key_label.after(1000, auto_key)
        else:
            count += 0
            Game.key_label.config(text="You have "+str(count)+" "+key_symb+"'s")
        
    def stop_auto_key():
        global running_auto_key
        running_auto_key = False
        
    def start_auto_key():
        global running_auto_key
        running_auto_key = True
        
    if count < time_Upgrade_list[0][0]:
        #pass
        tk.messagebox.showinfo(title="Information", message="Not enough keys")

    else:
        count = count - time_Upgrade_list[0][0]
        keys_per_sec = time_Upgrade_list[0][1]
        time_upgrade_count += 1
        
        time_Upgrade_list.remove(time_Upgrade_list[0])
        Upgrades.Time_Upgrade_button.config(text="Upgrade: "+str(time_Upgrade_list[0][1])+" Keys per Second\nCost: "+str(time_Upgrade_list[0][0])+" Keys")
        
        KeyboardClicker.show_frame(Game)
        if first_auto_key == True:
            auto_key()
            first_auto_key = False
        else:
            start_auto_key()

###############################################################################
    
###############################################################################

class Starting_frame(tk.Frame):
    
    def __init__(self, parent, controller):
        
        '''This function, __init__, within the object, Starting_frame, will
        display the opening screen for the game. It will show our team name
        and warn that we are not responsible for any increase in student
        procrastination. It will eventually disappear after 5 seconds and show
        the main menu.'''
        
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg="black")
        
        intro_statement = '''Welcome to Keyboard Clicker. This game was made for your
        entertainment developed by the students of TEAM 205C. Thank you for playing,
        and we hope you have a fun time!'''
        
        warning_statement = '''TEAM 205C is not responsible for any increase in student
        procrastination. Please play responsibly.'''
                             
        game_intro = tk.Label(self, text= intro_statement, bg="black", fg="white",)
        game_intro.pack(padx=5, pady= 10)
        
        warning_1 = tk.Label(self, text= "Warning!", bg="black", fg="red",
                           font="LARGE_FONT")
        warning_1.pack(padx=5, pady=20)
        
        warning_2 = tk.Label(self, text= warning_statement, bg="black",
                             fg="white")
        warning_2.pack(padx=5, pady=5)

###############################################################################

class Main_menu(tk.Frame):
    
  def __init__(self, parent, controller):    
        '''This function, __init__, within the object, Main_menu, will display
        the frame of the main menu for the game. It will have 4 buttons: Play,
        Checkpoint, Rules, and Quit. Pressing Quit will close the program
        completely.'''

        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg=bg_color)
        
        menu_title = tk.Label(self, text="Keyboard Clicker", bg=bg_color,
                             font=("LARGE_FONT", 18,"bold"))
        menu_title.pack(padx=5, pady=25)
        
        menu_play = tk.Button(self, text="Play/New Game", font = "LARGE_FONT",
                              bg="green", fg="black",
                              command=playGame)
        menu_play.pack(padx=5, pady=15)
        
        menu_resume = tk.Button(self, text="Resume", bg="black", fg="white", 
                                command=resumeGame)
        menu_resume.pack(padx=5, pady=15)
        
        menu_rules = tk.Button(self, text="Rules", bg="black", fg="white",
                               command=lambda: controller.show_frame(Rules))
        menu_rules.pack(padx=5, pady=5)
        
        menu_quit = tk.Button(self, text="Quit", bg="black", fg="white",
                              command=controller.destroy)
        menu_quit.pack(padx=5, pady=5)
        

###############################################################################

class Rules(tk.Frame):
    
    def __init__(self, parent, controller):
        
        '''This function, __init__, within the object, Rules, will display the
        frame containing the Rules. It will also allow for a path back to the
        main menu.'''
        
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg=bg_color)
        
        rules_label = tk.Label(self, text="Rules", font="LARGE_FONT",
                               bg=bg_color)
        rules_label.pack(padx=5, pady=10)
        
        with open("Keyboard_Clickers_rules.txt") as rules_file:
            instructions = rules_file.read()
            
            rules_ = tk.Label(self, text=instructions, bg=bg_color)
            rules_.pack(padx= 5, pady=25)
        
        rules_back_button = tk.Button(self, text="Back", bg="black",
                                    fg="white",
                                    command=lambda: controller.show_frame(Main_menu))
        rules_back_button.pack(padx=5, pady=10)
        
###############################################################################
class Game(tk.Frame):
    
    def __init__(self, parent, controller):
        
        '''This function,__init__, within the object, Game, will display the frame
        containing the main game of Keyboard Clicker. It will contain an upgrades
        button and a path back to the main menu.'''
        
        global count
        global count_num
        count_num=1
        count = 0
        
        def key_count():
            
            '''This function contains code that will increase the value of
            count by 1 every time the button is clicked.'''
            
            global count
            global count_num
            
            count += count_num
            Game.key_label.configure(text= "You have "+str(count)+" "+key_symb+"'s")
        
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg=bg_color)
        
        game_label_1 = tk.Label(self, text="Welcome to Keyboard Clicker!",
                                font="LARGE_FONT", bg=bg_color)
        game_label_1.pack(padx=5, pady=20)
        
        game_button = tk.Button(self, text="Click for " + '\U000026bf' + "'s!", bg="white",
                                relief=tk.RAISED,
                                font=("LARGE_FONT", 18, "bold"),
                                command= key_count)
        game_button.pack(padx=5, pady=25)
        
        Game.key_label = tk.Label(self, text= "You have "+str(count)+" "+key_symb+"'s",
                             font="LARGE_FONT", bg=bg_color)
        Game.key_label.pack(padx=5, pady=10)
        
        upgrade_button = tk.Button(self, text="Upgrades", font="LARGE_FONT",
        bg="black", fg="white", relief=tk.RAISED,
                                     command=lambda: controller.show_frame(Upgrades))
        upgrade_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        main_menu_button = tk.Button(self, text="Main Menu", font="LARGE_FONT",
                                     bg="black", fg="white", relief=tk.RAISED,
                                     command=lambda: controller.show_frame(Save_Frame))
        main_menu_button.pack(side=tk.RIGHT, padx=5, pady=5)

##############################################################################

def saveAndQuit():
    '''writes the number of clicks and upgrade information to a file'''
    def auto_key():
        global count
        global keys_per_sec
        global running_auto_key
        if running_auto_key == True:
            count += keys_per_sec
            Game.key_label.config(text="You have "+str(count)+" "+key_symb+"'s")
            Game.key_label.after(1000, auto_key)
        else:
            count += 0
            Game.key_label.config(text="You have "+str(count)+" "+key_symb+"'s")
            
        
    def stop_auto_key():
        global running_auto_key
        running_auto_key = False
        
    def start_auto_key():
        global running_auto_key
        running_auto_key = True
        
    with open(statusFile, 'w') as resumeFile:
        resumeFile.write(str(count)+','+str(count_num)+","+str(click_upgrade_count)+","+str(keys_per_sec)+","+str(time_upgrade_count))
    if overrideWindowXButton == False:
        KeyboardClicker.show_frame(Main_menu)
        stop_auto_key()
    else:
        KeyboardClicker.destroy()
        
##############################################################################

def closeWindow():
    '''if user selects no save after window x is pressed, the window should destroy itself'''
    if overrideWindowXButton == False:
        KeyboardClicker.show_frame(Main_menu)
    else:
        KeyboardClicker.destroy()

##############################################################################
    
def resumeGame():
    '''reads file created from function saveAndQuit function to allow game to resume'''
    global count
    global count_num
    global click_Upgrade_list
    global click_upgrade_count
    global keys_per_sec
    global time_upgrade_count
    global time_Upgrade_list
    global first_resume
    global first_auto_key
    
    count = 0
    count_num = 1
    click_Upgrade_list = [[100, 2], [1000, 3], [50000, 10], [100000, 35], [5000000, 50], [1000000000, 125]]
    click_upgrade_count = 0
    keys_per_sec = 0
    time_upgrade_count = 0
    time_Upgrade_list = [[100, 1], [1000, 2], [50000, 4], [100000, 9], [5000000, 25], [1000000000, 75]]
    first_auto_key = False
    
    def auto_key():
        global count
        global keys_per_sec
        global running_auto_key
        if running_auto_key == True:
            count += keys_per_sec
            Game.key_label.config(text="You have "+str(count)+" "+key_symb+"'s")
            Game.key_label.after(1000, auto_key)
        else:
            count += 0
            Game.key_label.config(text="You have "+str(count)+" "+key_symb+"'s")
        
    def stop_auto_key():
        global running_auto_key
        running_auto_key = False
        
    def start_auto_key():
        global running_auto_key
        running_auto_key = True
        
    if Path(statusFile).exists():
        with open(statusFile, 'r') as resumeFile:
            try:
                data_line = resumeFile.readline().split(",")
                count = int(data_line[0])
                count_num = int(data_line[1])
                click_upgrade_count = int(data_line[2])
                keys_per_sec = int(data_line[3])
                time_upgrade_count = int(data_line[4])
                
                if click_upgrade_count == 0:
                    pass
                else:
                    for i in range(click_upgrade_count):
                        click_Upgrade_list.remove(click_Upgrade_list[0])
                    Upgrades.Click_Upgrade_button.config(text="Upgrade: "+str(click_Upgrade_list[0][1])+" Keys per Click\nCost: "+str(click_Upgrade_list[0][0])+" Keys")
                    
                if time_upgrade_count == 0:
                    pass
                else:
                    for i in range(time_upgrade_count):
                        time_Upgrade_list.remove(time_Upgrade_list[0])
                    Upgrades.Time_Upgrade_button.config(text="Upgrade: "+str(time_Upgrade_list[0][1])+" Keys per Second\nCost: "+str(time_Upgrade_list[0][0])+" Keys")
                
                KeyboardClicker.show_frame(Game)
                if first_resume == True:
                    first_resume = False
                    start_auto_key()
                    auto_key()
                else:
                    start_auto_key()
                    auto_key()
            except:
                tk.messagebox.showinfo(title="Information", message="No saved game to resume")
    else:
      tk.messagebox.showinfo(title="Information", message="No saved game to resume")

##############################################################################

def playGame():
    '''resets the play window with zero keys'''
    global count
    global count_num
    global click_upgrade_count
    global count_Upgrade_list
    global time_Upgrade_list
    global keys_per_sec
    global time_upgrade_count
    count = 0
    count_num = 1
    keys_per_sec = 0
    click_upgrade_count = 0
    time_upgrade_count = 0
    click_Upgrade_list = [[100, 2], [1000, 3], [50000, 10], [100000, 35], [5000000, 50], [1000000000, 125]]
    time_Upgrade_list = [[100, 1], [1000, 2], [50000, 4], [100000, 9], [5000000, 25], [1000000000, 75]]
    Upgrades.Click_Upgrade_button.config(text="Upgrade: "+str(click_Upgrade_list[0][1])+" Keys per Click\nCost: "+str(click_Upgrade_list[0][0])+" Keys")
    Upgrades.Time_Upgrade_button.config(text="Upgrade: "+str(time_Upgrade_list[0][1])+" Keys per Second\nCost: "+str(time_Upgrade_list[0][0])+" Keys")
    KeyboardClicker.show_frame(Game)

##############################################################################

def overrideWindowX():
  '''disables the exit button and asks user if they want to save game or not'''
  global overrideWindowXButton
  overrideWindowXButton = True
  KeyboardClicker.show_frame(Save_Frame)
  
##############################################################################

def displaySavedCounter():
  '''This function displays the saved number of keys from the previous game'''
  Game.key_label.config(text= "You have "+str(count)+" "+key_symb+"'s")

##############################################################################

class Save_Frame(tk.Frame):
    def __init__(self, parent, controller):
        
        '''This function,__init__, within the object, Quit, will display the frame
           prompting the user to click the button yes or no to save the game. 
           Regardless of the selection, the window will close. '''
        
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg=bg_color)
        
        save_or_quit_label = tk.Label(self, text="Save Game?", font="LARGE_FONT",
                               bg=bg_color)
        save_or_quit_label.pack(padx=5, pady=10)
        
        yes_button = tk.Button(self, text="Yes", bg="black",
                                     fg="white",
                                     command=saveAndQuit)
        yes_button.pack(padx=5, pady=10)
        
        no_button = tk.Button(self, text="No", bg="black",
                                     fg="white",
                                     command=closeWindow)
        no_button.pack(padx=5, pady=10)
        
###############################################################################


help(KeyClick.__init__)
help(KeyClick.show_frame)
help(Main_menu.__init__)
help(Rules.__init__)
help(Game.__init__)
help(saveAndQuit)
help(resumeGame)
help(displaySavedCounter)
help(Save_Frame.__init__)
help(overrideWindowX)
help(closeWindow)

overrideWindowXButton = False
statusFile = "keyboard_clicker.dat"
KeyboardClicker = KeyClick()
KeyboardClicker.protocol('WM_DELETE_WINDOW', overrideWindowX)
KeyboardClicker.title("Keyboard Clicker")
KeyboardClicker.mainloop()


#Open keyboard clicker (graphic here?)
# Open main menu with two options:
	#A. Play
		#1. Start New
			#Click anywhere on the screen to gain a point
      #for each click, points+=1
      #When points==x, option to upgrade
      #if no, continue
      #if yes, subtract price of upgrade and add multiplier:
        #for each click, points+=1*factor
      #Option to save progress.
		#2. Checkpoint (file input)
      #continue with saved values
      #Click anywhere on the screen to gain a point
      #for each click, points+=1
      #When points==x, option to upgrade
      #if no, continue
      #if yes, subtract price of upgrade and add multiplier:
        #for each click, points+=1*factor
      #Option to save progress.
    #Option to quit or continue after saving
    #After quitting game, return to main menu
	#B. Rules (text file input)

''''
1. The Keyboard Clicker is based off of Cookie Clicker, a game where the user continuously presses a cookie to earn more keys and upgrades. Once the game starts, you will be prompted to click the space bar. The more you press the spacebar, the more keys you will earn. 
2. Once you have enough keys to purchase an upgrade, you will have the option to upgrade the multiplier for how many keys you get per click. 
3. If at any point you wish to save your progress, you will have the option to save your progress as an access code. 
'''''
'''
y='\U000026bf'
x='\U0001f5dd'

print(y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y,y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, "\nWarning = Team C is not responsible for any loss in student productivity \n\bnor increase in procrastination. Please enjoy responsibly.\n"+y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y,y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y, y)
'''

#######################################################################

######################################################

#import time at the top of repl
#time upgrade gives 'boost' of points over a set time duration
#duration/points of time upgrades flexible for change
#We can either update the count real time or at the end of duration 
import time
def Time_Upgrade():
  '''Upgrade1 gives points over 1000 sec''' #ROI roughly 800 points
  global count
  count = count - 100
  counter=0
  
  now = time.time()
  future = now + 10
  while time.time() < future:
    counter += 0.0001
    print(int('%.0f' % counter) + count) #just to see time upgrade in action
    count += counter #we can either update the global count at the end of the duration or during the timer
    pass
  command= lambda: controller.show_frame(Game)