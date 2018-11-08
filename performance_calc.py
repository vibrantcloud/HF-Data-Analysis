total_sale = 5000
total_forecast = 4021321321
total_performance = 25
minx = -20
variable_hours = -18

if total_sale > total_forecast and total_performance < 0:
    print(0)
elif total_performance >= 0:
    print(total_performance)
elif total_performance < minx and minx > variable_hours:
     print(minx)
elif total_performance < minx and minx < variable_hours:
    print(variable_hours)
elif total_performance > minx and total_performance > variable_hours:
    print(total_performance) 
elif total_performance > minx and total_performance < variable_hours:
    print(total_performance)
    
