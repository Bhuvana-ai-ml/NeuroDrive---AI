from risk.ttc import TTCEngine

ttc_engine = TTCEngine()

distance = 8
relative_speed = 5

ttc = ttc_engine.calculate_ttc(
    distance,
    relative_speed
)

risk = ttc_engine.risk_level(ttc)

print("Distance:", distance)
print("TTC:", ttc)
print("Risk:", risk)