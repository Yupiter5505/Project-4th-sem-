import SingleNumbers as SN


class TypeOfEffect:

    def __init__(self, effect, duration, ee=None, charge=None):
        self.effect = effect
        self.duration = duration
        self.ee = ee    # Extra Effect
        self.charge = charge


DurationOfEffects = SN.DurationOfEffects
KeyOfEffects = dict([
  ('Great damage per second', 3*SN.SingleDamage/5), ('Medium damage per second', 2*SN.SingleDamage/5),
  ('Low damage per second', SN.SingleDamage/5), ('Slowdown', SN.SingleVelocity/5),
])

Burning = TypeOfEffect('Great damage per second', DurationOfEffects, None, 3)
Slowdown = TypeOfEffect('Slowdown', DurationOfEffects)
Bleeding = TypeOfEffect('Low damage per second', DurationOfEffects, 'Increase of in-damage', 2)
Radiation = TypeOfEffect('Medium damage per second', DurationOfEffects, 'Epidemic')
Poison = TypeOfEffect('Low damage per second', DurationOfEffects, 'Amplification of effects', 5)

ListOfEffects = [Burning, Slowdown, Bleeding, Radiation, Poison]
