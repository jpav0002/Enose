from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d%m%Y_%H%M%S")
print("date and time =", dt_string)

# Minutes
minuto = now.minute
print("Minuto", minuto)

