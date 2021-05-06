from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Meal

class Calendar(HTMLCalendar):
	def __init__(self, date=None):
		self.date = date
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, date, meals):
		meals_per_date = meals.filter(start_time__date=date)
		d = ''
		for meal in meals_per_date:
			d += f'<li> {meal.title} </li>'

		if date != 0:
			return f"<td><span class='date'>{date}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, meals):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, meals)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter meals by year and month
	def formatmonth(self, withyear=True):
		meals = meal.objects.filter(meal_date=self.date)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		# cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, meals)}\n'
		return cal