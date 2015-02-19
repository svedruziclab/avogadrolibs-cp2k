"""
/******************************************************************************

  This source file is not yet a part of the Avogadro project.

Copyright 2015 Tomislav Subic <tomislav.subic@gmail.com>

  This source code is released under the New BSD License, (the "License").

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

******************************************************************************/
"""

import argparse
import json
import sys
import xml.etree.ElementTree as ET

# Some globals:
targetName = 'CP2K'
debug = False
# Number of valence electrons for each chemical element
valencee = {}
valencee['H'] = 1
valencee['He'] = 2
valencee['Li'] = 3
valencee['Be'] = 4
valencee['B'] = 3
valencee['C'] = 4
valencee['N'] = 5
valencee['O'] = 6
valencee['F'] = 7
valencee['Ne'] = 8
valencee['Na'] = 9
valencee['Mg'] = 10
valencee['Al'] = 3
valencee['Si'] = 4
valencee['P'] = 5
valencee['S'] = 6
valencee['Cl'] = 7
valencee['Ar'] = 8
valencee['K'] = 9
valencee['Ca'] = 10
valencee['Sc'] = 11
valencee['Ti'] = 12
valencee['V'] = 13
valencee['Cr'] = 14
valencee['Mn'] = 15
valencee['Fe'] = 16
valencee['Co'] = 17
valencee['Ni'] = 18
valencee['Cu'] = 11
valencee['Zn'] = 12
valencee['Ga'] = 13
valencee['Ge'] = 4
valencee['As'] = 5
valencee['Se'] = 6
valencee['Br'] = 7
valencee['Kr'] = 8
valencee['As'] = 5
valencee['Sr'] = 10
valencee['Y'] = 11
valencee['Zr'] = 12
valencee['Mo'] = 14
valencee['Ru'] = 16
valencee['Rh'] = 17
valencee['Pd'] = 18
valencee['Ag'] = 11
valencee['In'] = 13
valencee['Sb'] = 5
valencee['Te'] = 6
valencee['I'] = 7
valencee['Ba'] = 10
valencee['W'] = 14
valencee['Au'] = 11
valencee['Bi'] = 15

def getOptions():
  userOptions = {}

  userOptions['Title'] = {}
  userOptions['Title']['type'] = 'string'
  userOptions['Title']['default'] = ''

  userOptions['Grid number'] = {}
  userOptions['Grid number']['type'] = "integer"
  userOptions['Grid number']['minimum'] = 1
  userOptions['Grid number']['default'] = 4

  userOptions['Grid cutoff'] = {}
  userOptions['Grid cutoff']['type'] = "integer"
  userOptions['Grid cutoff']['minimum'] = 1
  userOptions['Grid cutoff']['default'] = 300

  userOptions['Grid rel cutoff'] = {}
  userOptions['Grid rel cutoff']['type'] = "integer"
  userOptions['Grid rel cutoff']['minimum'] = 1
  userOptions['Grid rel cutoff']['default'] = 60

  userOptions['Run Type'] = {}
  userOptions['Run Type']['type'] = "stringList"
  userOptions['Run Type']['default'] = 0
  userOptions['Run Type']['values'] = \
    ['Energy and forces','Geometry Optimization','Molecular dynamics'] #TODO: add the rest of run types

  userOptions['Method'] = {}
  userOptions['Method']['type'] = "stringList"
  userOptions['Method']['default'] = 1
  userOptions['Method']['values'] = \
    ['Electronic structure methods (DFT)','Molecular Mechanics' ,'Hybrid quantum classical (Not yet supported)']#TODO: add the rest of methods  userOptions['Method'] = {}

  userOptions['Basis Set'] = {}
  userOptions['Basis Set']['type'] = "stringList"
  userOptions['Basis Set']['default'] = 0
  userOptions['Basis Set']['values'] = \
     ['SZV-GTH','DZV-GTH','DZVP-GTH',   'TZVP-GTH', 'TZV2P-GTH']#TODO: add the rest of basis sets

  userOptions['Functional'] = {}
  userOptions['Functional']['type'] = "stringList"
  userOptions['Functional']['default'] = 1
  userOptions['Functional']['values'] = \
    ['BLYP','BP','HCTH120', 'PADE', 'PBE'] #TODO: add the rest of functionals

  userOptions['Filename Base'] = {}
  userOptions['Filename Base']['type'] = 'string'
  userOptions['Filename Base']['default'] = 'job'

  opts = {}
  opts['userOptions'] = userOptions
  opts['inputMoleculeFormat'] = 'cml'


  return opts
def generateElements(cml, unique=0):
  e = ET.fromstring(cml)
  elements = []
  for i in e:
    if ('atomArray' in i.tag):
      break
  atomArray = i

  for i in atomArray:
    elements.append(i.get('elementType'))
  if unique == 1:
    return set(elements)
  else: 
    return elements

def generateInputFile(cml, opts):
  global valencee
  # Extract options:
  title = opts['Title']
  calculate = opts['Run Type']
  method = opts['Method']
  basisSet = opts['Basis Set']
  functional = opts['Functional']
  ngrids = opts['Grid number']
  cutoff = opts['Grid cutoff']
  rel_cutoff = opts['Grid rel cutoff']

  # Preamble
  cp2kfile = ""
  cp2kfile += "&GLOBAL\n"
  cp2kfile += "  PROJECT %s \n"%title

  # Task TODO: add other run types
  cp2kfile += "  RUN_TYPE "
  if calculate == 'Energy and forces':
    cp2kfile += "ENERGY_FORCE"
  elif calculate == 'Molecular dynamics':
    cp2kfile += "MOLECULAR_DYNAMICS"
  elif calculate == 'Geometry Optimization':
    cp2kfile += "GEO_OPT"
  else:
    raise Exception("Invalid calculation type: %s"%calculate)
  cp2kfile += "\n"

  cp2kfile += "  PRINT_LEVEL LOW\n"
  cp2kfile += "&END GLOBAL\n\n"

  # Force evaluation
  cp2kfile += "&FORCE_EVAL\n"

  # Method
  cp2kfile += "  METHOD "
    # Task TODO: add other methods
  if method == 'Electronic structure methods (DFT)':
    cp2kfile += "QUICKSTEP"
  elif method == 'Hybrid quantum classical (Not yet supported)':
    cp2kfile += "QMMM"
  elif method == 'Molecular Mechanics':
    cp2kfile += "FIST"
  else:
    raise Exception("Invalid calculation type: %s"%method)
  cp2kfile += "\n"


  if method == 'Electronic structure methods (DFT)':
    cp2kfile += "  &SUBSYS\n"
    # Kind

    uniqueElements = generateElements(str(cml), 1)

    for i in uniqueElements:
      cp2kfile += "    &KIND " + str(i)
      cp2kfile += "\n      ELEMENT   " + str(i)
      cp2kfile += "\n      BASIS_SET   " + basisSet
      cp2kfile += "\n      POTENTIAL   GTH-"+functional+"-q"+str(valencee[str(i)])+"\n"
      cp2kfile += "    &END KIND\n"

    # Cell Angstrom
    cp2kfile += "    &CELL\n"
    cp2kfile += "    A     10.00000000    0.000000000    0.000000000\n"
    cp2kfile += "    B     0.000000000    10.00000000    0.000000000\n"
    cp2kfile += "    C     0.000000000    0.000000000    10.00000000\n"
    cp2kfile += "    &END CELL \n"

    # Coordinates
    cp2kfile += "    &COORD\n"
    cp2kfile +="$$coords:          S      x    y    z$$\n"
    cp2kfile += "    &END COORD\n\n"
    cp2kfile += "  &END SUBSYS\n"
    # DFT

    cp2kfile += "  &DFT\n"
    cp2kfile += "    BASIS_SET_FILE_NAME  BASIS_SET\n"
    cp2kfile += "    POTENTIAL_FILE_NAME  GTH_POTENTIALS\n"

    cp2kfile += "    &QS\n"
    cp2kfile += "      EPS_DEFAULT 1.0E-10\n"
    cp2kfile += "    &END QS\n"

    cp2kfile += "    &MGRID\n"
    cp2kfile += "      NGRIDS "+str(ngrids)+"\n"
    cp2kfile += "      CUTOFF "+str(cutoff)+"\n"
    cp2kfile += "      REL_CUTOFF "+str(rel_cutoff)+"\n"
    cp2kfile += "    &END MGRID\n"

    cp2kfile += "    &XC\n"
    cp2kfile += "      &XC_FUNCTIONAL "+functional+"\n"
    cp2kfile += "      &END XC_FUNCTIONAL\n"
    cp2kfile += "    &END XC\n"

    cp2kfile += "    &SCF\n"
    cp2kfile += "      SCF_GUESS ATOMIC\n"
    cp2kfile += "      EPS_SCF 1.0E-7\n"
    cp2kfile += "      MAX_SCF 300\n"
    cp2kfile += "      &DIAGONALIZATION\n"
    cp2kfile += "        ALGORITHM STANDARD\n"
    cp2kfile += "      &END DIAGONALIZATION\n"
    cp2kfile += "      &MIXING\n"
    cp2kfile += "        METHOD BROYDEN_MIXING\n"
    cp2kfile += "        ALPHA 0.4\n"
    cp2kfile += "        NBROYDEN 8\n"
    cp2kfile += "      &END MIXING\n"

    cp2kfile += "    &END SCF\n"

    cp2kfile += "  &END DFT\n"
    cp2kfile += "  &PRINT\n"
    cp2kfile += "    &FORCES ON\n"
    cp2kfile += "    &END FORCES\n"
    cp2kfile += "  &END PRINT\n"
#MM
  

  elif method == 'Molecular Mechanics':
    cp2kfile += "  &SUBSYS\n"

    # Cell Angstrom
    cp2kfile += "    &CELL\n"
    cp2kfile += "    A     10.00000000    0.000000000    0.000000000\n"
    cp2kfile += "    B     0.000000000    10.00000000    0.000000000\n"
    cp2kfile += "    C     0.000000000    0.000000000    10.00000000\n"
    cp2kfile += "    &END CELL \n"

    # Coordinates
    cp2kfile += "    &COORD\n"
    cp2kfile +="$$coords:          S      x    y    z$$\n"
    cp2kfile += "    &END COORD\n\n"
    cp2kfile += "    &TOPOLOGY\n"
    cp2kfile += "      CHARGE_BETA\n"
    cp2kfile += "      CONNECTIVITY AMBER\n"
    cp2kfile += "      CONN_FILE_NAME ! Add file name that contains connectivity data\n"
    cp2kfile += "    &END TOPOLOGY \n"

    cp2kfile += "    &PRINT\n"
    cp2kfile += "      &TOPOLOGY_INFO\n"
    cp2kfile += "        AMBER_INFO\n"
    cp2kfile += "      &END\n"
    cp2kfile += "    &END \n"

    cp2kfile += "  &END SUBSYS\n"

    cp2kfile += "  &MM\n"

    cp2kfile += "    &FORCEFIELD\n"
    cp2kfile += "      ! Add file name that contains force field parameters\n"
    cp2kfile += "      parmtype AMBER\n"
      
    cp2kfile += "      &SPLINE\n"
    cp2kfile += "        EMAX_SPLINE 10000\n"
    cp2kfile += "      &END SPLINE\n"
    cp2kfile += "    &END FORCEFIELD\n"

    cp2kfile += "    &POISSON\n"
    cp2kfile += "      &EWALD\n"
    cp2kfile += "        EWALD_TYPE SPME\n"
    cp2kfile += "        ALPHA .36\n"
    cp2kfile += "        GMAX 128\n"
    cp2kfile += "      &END EWALD\n"
    cp2kfile += "    &END POISSON\n"

    cp2kfile += "    &PRINT\n"
    cp2kfile += "      &FF_INFO\n"
    cp2kfile += "      $END\n"
    cp2kfile += "      &FF_PARAMETER_FILE\n"
    cp2kfile += "      &END\n"
    cp2kfile += "    &END PRINT\n"

    cp2kfile += "  &END MM\n"



  cp2kfile += "&END FORCE_EVAL\n"

  return cp2kfile

def generateInput():
  # Read options from stdin
  stdinStr = sys.stdin.read()

  # Parse the JSON strings
  opts = json.loads(stdinStr)

  # Generate the input file
  inp = generateInputFile(opts['cml'], opts['options'])

  # Basename for input files:
  baseName = opts['options']['Filename Base']

  # Prepare the result
  result = {}
  # Input file text -- will appear in the same order in the GUI as they are
  # listed in the array:
  files = []
  files.append({'filename': '%s.inp'%baseName,
                'contents': inp})

  if debug:
    files.append({'filename': 'debug_info', 'contents': stdinStr})
  result['files'] = files
  # Specify the main input file. This will be used by MoleQueue to determine
  # the value of the $$inputFileName$$ and $$inputFileBaseName$$ keywords.
  result['mainFile'] = '%s.inp'%baseName
  return result

if __name__ == "__main__":
  parser = argparse.ArgumentParser('Generate a a %s input file.'%targetName)
  parser.add_argument('--debug', action='store_true')
  parser.add_argument('--print-options', action='store_true')
  parser.add_argument('--generate-input', action='store_true')
  parser.add_argument('--display-name', action='store_true')
  args = vars(parser.parse_args())

  debug = args['debug']

  if args['display_name']:
    print(targetName)
  if args['print_options']:
    print(json.dumps(getOptions()))
  elif args['generate_input']:
    print(json.dumps(generateInput()))
