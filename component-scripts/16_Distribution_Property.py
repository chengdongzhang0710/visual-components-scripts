form vcScript import *

# print out all the seed values
app = getApplication()
streams = app.findLayoutItem("RandomSeeds")
for p in streams.Properties:
  print p.Name, p.Value

# change corresponding seed value
streams.RandomSeed10 = 400

comp = getComponent()
prop = comp.getProperty("Test_Distribution")
if not prop:
  prop = comp.createProperty(VC_DISTRIBUTION, "Test_Distribution")

prop.Distribution = "normal(10.0, 2.0)"

# each layout item has 64 streams, each stream has its own seed value (by default they are the same)
prop.RandomStream = 10  # 0 ~ 63

# prop.Distribution = "normal(50, 10.0, 2.0)"  # the first argument is equivalent to prop.RandomStream = 50

# prop.Distribution = "normal(70, 10.0, 2.0)"  # if use the stream not existed in the layout, you will get differnent set of numbers every time you run the simulation

def OnRun():
  print "--------------------"
  for _ in range(5):
    print prop.Value  # -> get the same five numbers every time run the simulation, because stream with a seed value
