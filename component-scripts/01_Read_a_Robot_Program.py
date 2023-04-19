# You can move functions into a new Python file and paste it into the Visual Components My Commands folder
# You can import functions in My Commands folder by "from {fileName} import *" directly in other Python Script

from vcScript import *

comp = getComponent()

# robotExecutor = comp.findBehaviour("Executor")  # can find its name in component graph
robotExecutor = comp.findBehavioursByType("rRobotExecutor")[0]

robotProgram = robotExecutor.Program

# routines
mainRoutine = robotProgram.MainRoutine

subRoutines = robotProgram.Routines

# local variables defined in main routine or other sub routines
for property in mainRoutine.Properties:
  print property.Name

# statements
statements = mainRoutine.Statements

for statement in statements:
  if statement.Scopes:
    for scope in statements.Scopes:
      print scope.Statements

# define a function to capture all statements in main routine or other sub routines
def getAllStatementsInRoutine(scope, statements=None):
  if not statements:
    statements = []
  
  for statement in scope.Statements:
    statements.append(statement)

    if statement.Scopes:
      for scope in statement.Scopes:
        getAllStatementsInRoutine(scope, statements)
  
  return statements

print len(getAllStatementsInRoutine(mainRoutine))
print len(getAllStatementsInRoutine(subRoutines[0]))

# defined a function to capture all statements called by the robot program
def getAllStatementsInRobotProgram(program):
  statements = getAllStatementsInRoutine(program.MainRoutine)

  for statement in statements:
    subRoutine = statement.getProperty("Routine")
    if subRoutine:
      getAllStatementsInRoutine(subRoutine.Value, statements)
  
  return statements

print len(getAllStatementsInRobotProgram(robotProgram))

# motion positions
positions = []
for statement in subRoutines[0].Statements:
  try:
    print statement.Positions
  except:
    continue

# define a function to capture all positions in main routine or other sub routines
def getAllPositionsInRountine(scope):
  statements = getAllStatementsInRoutine(scope)

  positions = []
  for statement in statements:
    try:
      # for position in statement.Positions:
      #   positions.append(position)
      positions.extend(statement.Positions)
    except:
      pass
  
  return positions

print getAllPositionsInRountine(mainRoutine)

for subRoutine in subRoutines:
  print getAllPositionsInRountine(subRoutine)

# define a function to capture all positions in robot program
def getAllPositionsInRobotProgram(program):
  positions = getAllPositionsInRountine(program.MainRoutine)

  for subRoutine in program.Routines:
    positions.extend(getAllPositionsInRountine(subRoutine))
  
  return positions

print len(getAllPositionsInRobotProgram(robotProgram))
