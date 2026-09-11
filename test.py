# @Author: Sheep Wang
# @File: test.py
# @Created: 2026-09-04 23:27
# @Description: test.py


li = ["tt", "CC", "AA"]

sql = "select * from mm"

ff = " where " + " AND ".join(li)

print(ff)
