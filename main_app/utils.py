
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Meal

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, meals):
		meals_per_day = meals.filter(date__day=day)
		d = ''
		for meal in meals_per_day:

			if meal.meal == 'B':
				d += f'<div><li style ="background-color: pink; width:200px;margin: 0;"> {meal.meal}: <a href="{ meal.recipe_url }" target="_blank"> {meal.recipe_name} </li></div><br>'
			elif meal.meal == 'R':
				d += f'<div><li style ="background-color: yellow; width:200px;margin: 0;"> {meal.meal}: <a href="{ meal.recipe_url }" target="_blank"> {meal.recipe_name} </li></div><br>'
			elif meal.meal == 'L':
				d += f'<div><li style ="background-color: orange; width:200px;margin: 0;"> {meal.meal}: <a href="{ meal.recipe_url }" target="_blank"> {meal.recipe_name} </li></div><br>'
			else:
				d += f'<div><li style ="background-color: blue; width:200px;margin: 0;"> {meal.meal}: <a href="{ meal.recipe_url }" target="_blank"> {meal.recipe_name} </li></div><br>'

		if day != 0:
			return f'<td style="vertical-align: top;text-align: left;"><span class="date">{day}</span><ul> {d} </ul></td>'
		return '<td style ="width:200px"></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, meals):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, meals)
		return f'<tr style="height:250px;"> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		meals = Meal.objects.filter(date__year=self.year, date__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, meals)}\n'
		return cal