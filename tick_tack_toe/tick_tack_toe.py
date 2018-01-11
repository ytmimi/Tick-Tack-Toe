import tkinter as tk
import sys
from collections import namedtuple
import random


def center_window(window, width, height):
	'''Centers the window in the middle of the screen'''
	screen_w = window.winfo_screenwidth()
	screen_h = window.winfo_screenheight()
	geometry=('{}x{}+{}+{}'.format(width, height, int(screen_w/2 - width/2), int(screen_h/2- height/2)))
	window.geometry(geometry)



#class that runs the game
class Game(tk.Tk):
	def __init__(self, width, height):
		super().__init__()
		self.title('Tick Tack Toe')
		self.width = width
		self.height = height
		self.sb_height = 30
		self.start_screen = self.create_start_screen()
		self.player1 = None
		self.player2 = None
		self.player_list= None
		self.score_board = None
		self.board = None
		center_window(self, self.width, self.height+2*self.sb_height)
		super().mainloop()

	def get_active_player(self):
		for player in self.player_list:
			if player.turn:	
				return player

	def change_player_turns(self):
		for player in self.player_list:
			if player.turn:
				player.change_turn()
			else:
				player.change_turn()

	def new_game(self, width, height):
		self.board.destroy()
		self.board = Game_Board(self, width, height)
		self.board.pack()

	def exit_game(self):
		sys.exit()

	def create_start_screen(self):
		return Start_Screen(self,self.width, self.height+self.sb_height)

	def back_to_main_menu(self):
		self.board.destroy()
		self.score_board.destroy()
		self.start_screen = self.create_start_screen()

	def create_player(self, **kwargs):
		return Player(**kwargs)

	def create_player_list(self):
		return [self.player1, self.player2]



#canvas for the board
class Game_Board(tk.Canvas):
	def __init__(self, master, width, height):
		self.master = master
		self.width = width
		self.height = height
		super().__init__(self.master, width=self.width, height=self.height)
		self.draw_board()
		self.bind("<Button-1>", self.update_board)
		#ADD a Function when the enter key is pressed that brings up the menue
		self.game_logic = Game_Logic(self.master)
		self.pack()

	def draw_board(self):
		''' Draws the Lines for the Tick Tack Toe board'''
		#horizontal lines (x1, y1, x2, y2)
		self.create_line(0, (1/3)*self.height, self.width, (1/3)*self.height)
		self.create_line(0, (2/3)*self.height, self.width, (2/3)*self.height)
		#vertical lines(x1, y1, x2, y2)
		self.create_line((1/3)*self.width, 0, (1/3)*self.width, self.height)
		self.create_line((2/3)*self.width, 0, (2/3)*self.width, self.height)

	def update_cell_if_empty(self,cell_index, x_center, y_center):
		board_cell = self.game_logic.get_board_cell(cell_index)
		if board_cell.empty:
			player = self.master.get_active_player()
			color = player.color
			player.draw_symbol(self,x_center, y_center, color)
			self.game_logic.update_board(cell_index, player.symbol, player.name)
			self.master.change_player_turns()
			self.master.score_board.update_scoreboard_turn()

	def check_game_over(self):
		#is_game_over function sets the has_winner and has_tie values
		#if there is a winner or if there is a tie 
		self.game_logic.is_game_over()
		if self.game_logic.has_winner:
			msg = '{} Wins!'.format(self.game_logic.winner)
			self.update_win_loss_record(self.game_logic.winner)
			self.game_over_window(msg)
		elif self.game_logic.has_tie:
			msg = 'Tie Game!'
			self.update_tie_record()
			self.game_over_window(msg)
	
	def update_tie_record(self):
			self.master.player1.update_tie()
			self.master.player2.update_tie()
			self.master.score_board.update_score_board()

	def update_win_loss_record(self, winner):
		for player in self.master.player_list:
			if player.name == winner:
				player.update_wins()
			else:
				player.update_loss()
		self.master.score_board.update_score_board()
	
	def game_over_window(self, msg):
		x1 = (3/6)*self.width
		y1 = (2/6)*self.height
		window = Game_Over_Frame(self.master, msg)
		self.create_window(x1, y1, window=window)

	def update_board(self, event):
		'''Updates the game board is the cell is empty'''
		x_pos = event.x
		y_pos = event.y
		w = self.width
		h = self.height
		
		#if the game isn't over
		if not self.game_logic.game_over:
			#checks to see if the x positon is bounded in the first 1/3 of the board 
			if 0 <= x_pos < (1/3)*self.width:
				#checks to see if the y position is bounded in the first 1/3
				if 0 <= y_pos < (1/3)*self.height:
					self.update_cell_if_empty(1, (1/6)*w, (1/6)*h)
				#checks to see if the y position is bounded in the middle 1/3
				elif (1/3)*self.height <= y_pos < (2/3)*self.height:
					self.update_cell_if_empty(4, (1/6)*w, (3/6)*h)
				#else the y position is in the final 1/3
				else:
					self.update_cell_if_empty(7, (1/6)*w, (5/6)*h)
			#checks to see if the x positon is bounded in the middle 1/3 of the board 
			elif (1/3)*self.width <= x_pos < (2/3)*self.width:
				#checks to see if the y position is bounded in the first 1/3
				if 0 <= y_pos < (1/3)*self.height:
					self.update_cell_if_empty(2, (3/6)*w, (1/6)*h)
				#checks to see if the y position is bounded in the middle 1/3
				elif (1/3)*self.height <= y_pos < (2/3)*self.height:
					self.update_cell_if_empty(5, (3/6)*w, (3/6)*h)
				#else the y position is in the final 1/3
				else:
					self.update_cell_if_empty(8, (3/6)*w, (5/6)*h)
			#else the x position is in the final 1/3
			else:
				#checks to see if the y position is bounded in the first 1/3
				if 0 <= y_pos < (1/3)*self.height:
					self.update_cell_if_empty(3, (5/6)*w, (1/6)*h)
				#checks to see if the y position is bounded in the middle 1/3
				elif (1/3)*self.height <= y_pos < (2/3)*self.height:
					self.update_cell_if_empty(6, (5/6)*w, (3/6)*h)
				#else the y position is in the final 1/3
				else:
					self.update_cell_if_empty(9, (5/6)*w, (5/6)*h)
			
			#after updateing the board, check if the game is over
			self.check_game_over()




class Player():
	def __init__(self, symbol, turn, name, color='black'):
		self.symbol = symbol
		self.turn = turn
		self.name = name
		self.color = color
		self.draw_func = Board_Symbols(self.symbol).draw_symbol()
		self.wins = 0
		self.losses = 0
		self.ties = 0

	def change_turn(self):
		if self.turn:
			self.turn = False
		else:
			self.turn = True

	def draw_symbol(self,*args):
		#Symbol is determind in the Board_Symbols class
		self.draw_func(*args)

	#Add functions that update the players record
	def update_wins(self):
		self.wins += 1

	def update_loss(self):
		self.losses += 1

	def update_tie(self):
		self.ties += 1

	def player_score(self):
		return '{}-{}-{}'.format(self.wins, self.ties, self.losses)

		


class Game_Logic():
	Game_Data = namedtuple('Game_Data','empty symbol name') 
	def __init__(self, master):
		self.master = master
		self.logic_board = self.create_logic_board()
		self.has_winner = False
		self.has_tie = False
		self.game_over = False
		self.winner = None

	def create_logic_board(self):
		data_dict = {}
		for i in range(9):
			data_dict[i+1] = Game_Logic.Game_Data(True, None, None)
		# import pdb; pdb.set_trace()
		return data_dict

	def get_board_cell(self, index):
		return self.logic_board[index]
	
	def update_board(self, index, new_s, new_n):
		'''The game board data is updated with a new symbol and a new name'''
		new_cell =self.get_board_cell(index)._replace(empty=False, symbol=new_s, name=new_n)
		self.logic_board[index] = new_cell

	def check_win(self):
		'''Check to see if a winning combination is on the board'''
		cell_1 = self.get_board_cell(1)
		cell_2 = self.get_board_cell(2)
		cell_3 = self.get_board_cell(3)
		cell_4 = self.get_board_cell(4)
		cell_5 = self.get_board_cell(5)
		cell_6 = self.get_board_cell(6)
		cell_7 = self.get_board_cell(7)
		cell_8 = self.get_board_cell(8)
		cell_9 = self.get_board_cell(9)

		if cell_1.symbol == cell_2.symbol == cell_3.symbol !=None:
			self.winner = cell_1.name
			self.has_winner = True
			self.game_over = True
		elif cell_4.symbol == cell_5.symbol == cell_6.symbol !=None:
			self.winner = cell_4.name
			self.has_winner = True
			self.game_over = True
		elif cell_7.symbol == cell_8.symbol == cell_9.symbol !=None:
			self.winner = cell_7.name
			self.has_winner = True
			self.game_over = True
		elif cell_1.symbol == cell_5.symbol == cell_9.symbol !=None:
			self.winner = cell_1.name
			self.has_winner = True
			self.game_over = True
		elif cell_3.symbol == cell_5.symbol == cell_7.symbol !=None:
			self.winner = cell_3.name
			self.has_winner = True
			self.game_over = True
		elif cell_1.symbol == cell_4.symbol == cell_7.symbol !=None:
			self.winner = cell_1.name
			self.has_winner = True
			self.game_over = True
		elif cell_2.symbol == cell_5.symbol == cell_8.symbol !=None:
			self.winner = cell_2.name
			self.has_winner = True
			self.game_over = True
		elif cell_3.symbol == cell_6.symbol == cell_9.symbol !=None:
			self.winner = cell_3.name
			self.has_winner = True
			self.game_over = True

	def check_tie(self):
		'''Check to see if the players have tied'''
		empty_cell = [cell.empty for cell in self.logic_board.values() if cell.empty]
		if (len(empty_cell) == 0) and not self.has_winner:
			self.game_over_message = 'Tie Game!'
			self.has_tie = True
			self.game_over = True
			
	def is_game_over(self):
		self.check_win()
		self.check_tie()




class Game_Over_Frame(tk.Frame):
	def __init__(self, master, message):
		self.master = master
		self.message = message
		super().__init__(self.master)
		self.config(bd=3, relief=tk.GROOVE)
		self.label = tk.Label(self, text=self.message)
		self.label.pack()
		self.quit_btn = tk.Button(self, text='Quit',command=lambda: self.master.exit_game())
		self.quit_btn.pack(fill=tk.X)
		self.restart_btn = tk.Button(self, text='New Game', command= lambda: self.master.new_game(master.width, master.height))
		self.restart_btn.pack(fill=tk.X)
		self.main_menue_btn = tk.Button(self, text='Main Menu', command= lambda: self.master.back_to_main_menu())
		self.main_menue_btn.pack(fill=tk.X)




class Score_Board(tk.Frame):
	def __init__(self, master, height):
		self.master = master
		self.height = height
		self.width = self.master.width
		super().__init__(self.master)
		self.config(bd=3, relief=tk.GROOVE, height=self.height, width=self.width)
		self.pack(fill=tk.BOTH)
		self.turn = tk.Label(self,text='Turn: {}'.format(self.master.get_active_player().name))
		self.turn.pack()
		self.p1_name = self.master.player1.name
		self.p2_name = self.master.player2.name
		self.p1_score = tk.Label(self,text='{}: {}'.format(self.p1_name, self.master.player1.player_score()))
		self.p1_score.pack(side=tk.LEFT)
		self.p2_score = tk.Label(self,text='{}: {}'.format(self.p2_name, self.master.player2.player_score()))
		self.p2_score.pack(side=tk.RIGHT)
		
	def update_score_board(self):
		self.p1_score['text'] = '{}: {}'.format(self.p1_name, self.master.player1.player_score())
		self.p2_score['text'] = '{}: {}'.format(self.p2_name, self.master.player2.player_score())

	def update_scoreboard_turn(self):
		self.turn['text'] = 'Turn: {}'.format(self.master.get_active_player().name)




class Start_Screen(tk.Canvas):
	def __init__(self,master, width, height):
		self.master = master
		self.width = width
		self.height = height
		self.on_screen = True
		self.x_list = [int((x/36)*self.width) for x in range(1,36)]
		self.y_list = [int((y/36)*self.height) for y in range(1,36)]
		self.coordinates = []
		super().__init__(self.master, width=self.width, height=self.height)
		self.text = self.screen_text((1/2)*self.width, (1/6)*self.height, 'Tick Tack Toe')
		self.player1_frame = self.create_player_frame((2/9)*self.width, (5/12)*self.height, self.width, self.height, name='Player 1')
		self.player2_frame = self.create_player_frame((7/9)*self.width, (5/12)*self.height, self.width, self.height,name='Player 2')
		self.start_button = self.create_button((7/18)*self.width, (7/9)*self.width, 'Start', self.start_game)
		#Need to work on the info Button function
		self.info_button = self.create_button((11/18)*self.width, (7/9)*self.width, 'Info', self.game_info)
		self.symbols = Board_Symbols()
		self.pack()
		self.update_screen()

	def create_player_frame(self, x1, y1, width, height, name):
		player_frame = Player_Frame(self.master,(1/3)*width, (1/3)*height, name )
		self.create_window(x1, y1, window=player_frame)
		return player_frame

	def create_button(self,x1, y1, text, func, *args):
		button = tk.Button(self, text=text, command= lambda: func(*args))
		button.config(width=5, relief=tk.GROOVE)
		self.create_window(x1,y1, window=button)
		return button

	def screen_text(self, x1, y1, text):
		screen_text = self.create_text(x1,y1, text=text)
		return screen_text

	def update_screen(self):
		if self.on_screen:
			x1 = random.choice(self.x_list)
			y1 = random.choice(self.y_list)
			x2 = random.choice(self.x_list)
			y2 = random.choice(self.y_list)
			color1 = random.choice(self.player1_frame.color_options)
			color2 = random.choice(self.player2_frame.color_options)
			if (x1,y1) not in self.coordinates:
				self.symbols.draw_x(self,x1, y1, color1, scale=(1/64))
				self.coordinates.append((x1, y1))
			if(x2,y2) not in self.coordinates:
				self.symbols.draw_o(self,x2, y2, color2, scale=(1/64))
				self.coordinates.append((x2, y2))
			self.master.after(3000, self.update_screen)

	def start_game(self):
		#Randomly chooses who goes first
		goes_first = [True, False]
		p1_turn = goes_first.pop(random.choice(goes_first))
		p2_turn = goes_first[0]

		#gets the name of each player
		p1_name = self.player1_frame.get_player_entry()
		p2_name = self.player2_frame.get_player_entry()

		#gets the player symbol
		p1_sym = self.player1_frame.get_symbol_choice()
		p2_sym = self.player2_frame.get_symbol_choice()

		#ckecks if valid symbols were chosen for player 1 and player 2
		if self.check_valid_sym(p1_sym, p2_sym, p1_name, p2_name):
			#gets the color
			color1 = self.player1_frame.get_color_choice()
			color2 = self.player2_frame.get_color_choice()

			#creates the master player objects
			self.master.player1 = self.master.create_player(symbol=p1_sym, turn = p1_turn, name =p1_name, color=color1)
			self.master.player2 = self.master.create_player(symbol=p2_sym, turn = p2_turn, name =p2_name, color= color2)
			self.master.player_list = self.master.create_player_list()

			#destroy the current canvas and creats the scoreboard and gameboard
			self.master.score_board = Score_Board(self.master, self.master.sb_height)
			self.master.board = Game_Board(self.master, self.master.width, self.master.height)
			self.on_screen = False
			self.destroy()

	def check_valid_sym(self,sym1,sym2, name1, name2):
		default = self.player1_frame.get_default_symbol()
		if ((sym1 == default or sym2 == default) and (sym1==sym2)):
			msg = 'Select a choice for \n{} and {} '.format(name1, name2)
			invalid_choice_window((3/6)*self.width, (1/6)*self.height, msg)
			return False
		elif(sym1 == sym2):
			msg = '{} and {} can\'t \nhave the same symbol'.format(name1, name2)
			invalid_choice_window((3/6)*self.width, (1/6)*self.height, msg)
			return False
		elif sym1 == default:
			msg = 'Select a choice for: \n{}'.format(name1)
			invalid_choice_window((3/6)*self.width, (1/6)*self.height, msg)
			return False
		elif sym2 == default:
			msg = 'Select a choice for: \n {}'.format(name2)
			invalid_choice_window((3/6)*self.width, (1/6)*self.height, msg)
			return False
		else:
			return True

	def game_info(self):
		'''Takes you to the info screen'''
		#need to work on this function
		print('info')




class Player_Frame(tk.Frame):
	'''Player Setup Window Sets the values that 
	will ultimately be passed to the Player class constructor'''
	def __init__(self,master, width, height, name):
		self.master = master
		self.width = width
		self.height = height
		self.name = name
		super().__init__(self.master, width=self.width, height=self.height)
		self.config(bd=3, relief= tk.GROOVE)
		self.player_name = self.make_player_entry(master=self, caption=self.name, width=10)
		self.player_name.grid(row=0, column=1)
		self.symbol_options = ['Classic: x', 'Classic: o', 'Custom: :)']
		self.s_options = Option_Menu(self, 'Choose Symbol!',self.symbol_options)
		self.s_options.grid(row=1, column=0, columnspan=2)
		self.color_options = ['black', 'blue', 'red', 'green', 'brown']
		self.c_options = Option_Menu(self, 'black', self.color_options)
		self.c_options.grid(row=2, column=0, columnspan=2)
		self.display_btn = tk.Button(self, text='Display symbol', command= lambda :self.dispay_player_choice())
		self.display_btn.grid(row=3, column=0, columnspan=2)
		self.symbol_display = Symbol_Display(self, self.width, self.width)
		self.symbol_display.grid(row=4, column=0, columnspan=2, sticky=tk.S+tk.W+tk.E)
		self.pack()
	
	def make_player_entry(self,master, caption, width):
		tk.Label(master, text=caption).grid(row=0, column=0)
		entry = tk.Entry(master)
		if width:
			entry.config(width=width)
		return entry

	def get_player_entry(self):
		if self.player_name.get() == '':
			return self.name
		else:
			return self.player_name.get()

	def get_symbol_choice(self):
		return self.s_options.get_value()

	def get_default_symbol(self):
		return self.s_options.get_default_value()

	def get_color_choice(self):
		return self.c_options.get_value()

	def dispay_player_choice(self):
		# import pdb; pdb.set_trace()
		color = self.get_color_choice()
		sym = self.get_symbol_choice()
		def_sym = self.get_default_symbol()
		if sym != def_sym:
			func = Board_Symbols(sym).draw_symbol()
			self.symbol_display.draw_symbol(func, color)




class Option_Menu(tk.OptionMenu):
	def __init__(self, master, default, option_list):
		self.var = tk.StringVar()
		self.default = default
		self.var.set(self.default)
		self.options = option_list
		self.master = master
		super().__init__(self.master, self.var, *self.options)

	def get_value(self):
		symbol = self.var.get().split(' ')[-1]
		return symbol

	def get_default_value(self):
		symbol = self.default.split(' ')[-1]
		return symbol




class Symbol_Display(tk.Canvas):
	'''Canvas displaying the players symbol choice'''
	def __init__(self, master, width, height):
		self.master = master
		self.width = int(width)
		self.height = int(height)
		self.x = (1/2)*self.width
		self.y = (2/6)*self.height
		super().__init__(self.master, width = (2/6)*self.width, height = (2/6)*self.height)
		self.config(bd=3, relief= tk.GROOVE)

	def draw_symbol(self, func, color):
		self.delete('all')
		func(self, self.x, (1/2)*self.y, color, scale=(1/9))




class invalid_choice_window(tk.Tk):
	'''Pop up window that appears if there is a conflict with the players choices'''
	def __init__(self, width, height, message):
		self.width = width
		self.height = height
		self.message = message
		super().__init__()
		self.title('Error!!')
		self.label = tk.Label(self,text=message)
		self.label.config(wraplength = 300, padx=20)
		self.label.pack()
		self.btn = tk.Button(self, text='close', command=lambda: self.destroy())
		self.btn.pack()
		center_window(self, int(self.width), int(self.height))
		self.mainloop()




class Board_Symbols():
	'''Contains all the functions responsible for drawing player symbols'''
	def __init__(self, symbol='x'):
		self.symbol = symbol
		#If You Add more symbols, make sure to incude the acompany function 
		#in the function_options list and incude the symbols in the Player Frame class
		self.symbol_options = ['x', 'o', ':)']
		self.function_options = [self.draw_x, self.draw_o, self.draw_smile]

	def draw_symbol(self):
		sym_index = self.symbol_options.index(self.symbol)
		return self.function_options[sym_index]

	def draw_x(self,canvas, x,y, color, scale=(1/9)):
		'''Draws a cross at the given center x,y location'''
		w = int(scale*canvas.width)
		h = int(scale*canvas.height)
		canvas.create_line(x-w, y-h, x+w, y+h, fill = color)
		canvas.create_line(x-w, y+h, x+w, y-h, fill = color)
	
	def draw_o(self,canvas, x,y, color, scale=(1/9)):
		''' Draws a circle at the given center x, y location'''
		w = int(scale*canvas.width)
		h = int(scale*canvas.height)
		canvas.create_oval(x-w, y-h, x+w, y+h ,outline = color)

	def draw_smile(self,canvas, x,y, color, scale=(1/9)):
		''' Draws a smily face to the screen centered at the given x, y location'''
		big_w = int(scale*canvas.width)
		big_h = int(scale*canvas.height)
		small_w = int(scale*(1/4)*canvas.width)
		small_h = int(scale*(1/4)*canvas.height)
		eye1_x = int(x-scale*(1/3)*canvas.width)
		eye2_x = int(x+scale*(1/3)*canvas.width)
		eye_y = int(y-scale*(1/3)*canvas.height)
		mouth_y = int(y+scale*(1/2)*canvas.height)
		#the face
		canvas.create_oval(x-big_w, y-big_h, x+big_w, y+big_h ,outline = color, fill=color)
		#eye shifted to the left
		canvas.create_oval(eye1_x-small_w, eye_y-small_h, eye1_x+small_w, eye_y+small_h, fill='white', outline='white')
		#eye shifted to the right
		canvas.create_oval(eye2_x-small_w, eye_y-small_h, eye2_x+small_w, eye_y+small_h, fill='white', outline='white')
		#the right mouth
		canvas.create_arc(eye1_x-small_w, y, eye2_x+small_w, mouth_y, fill='white', outline='white', style = tk.PIESLICE, start=180.0)
		#the left mouth
		canvas.create_arc(eye1_x-small_w, mouth_y, eye2_x+small_w, y,  fill='white', outline='white', style = tk.PIESLICE, start=270.0)

if __name__ == '__main__':
	Game(500, 500)











