# TODO: Implementar vista de horarios.
#       Cuadro Derecho, Calculos de Una vez:
#
#       
#       - Poner los tipos de clase que se imparten y su repeticion.
#       - Poner el porcentaje de acertividad en relacion tipo de salon y tipo de clase.
# CSV: Obtener los edificios adecuadamente a la espear de nuev aversion del CSV

# | ----------------------------------------------------------------------- |
# | Imports          |

import os
import sys
import time
import math
import textwrap # used to mantain the text indent without affecting the text

import psycopg2    # pip install psycopg2-binary

import pandas as pd
from datetime import time as dtime

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QWidget, QGraphicsDropShadowEffect, QVBoxLayout, QPushButton, QGridLayout, QSizePolicy, QToolTip, QStyleFactory

from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QThread
from PyQt5.QtGui import QPixmap, QCursor, QFontDatabase, QFont, QColor

# | Global Variables |

COLORS = {
    'darkblue'  : "rgb(41, 45, 65)",
    'navyblue'  : "rgb(56, 64, 93)",
    'blue'      : "rgb(76, 84, 109)",
    'greyblue'  : "rgb(118, 126, 153)",
    'cyan'      : "rgb(116,124,156)",
    'whitegrey' : "rgb(212, 216, 224)",
    'grey'      : "rgb(150, 155, 165)",
    'white'     : "rgb(255, 255, 255)",
    'yellow'    : "rgb(252,204,92)",
    'red'       : "rgb(124,4,4)"
}

# These are fixes sizes to the pixel art works
MINWINDOWWIDTH  = 800
MINWINDOWHEIGHT = 450
MINWINDOWMARGIN = 0
MINBUTTONWIDTH  = 320
MINBUTTONHEIGHT = 160
MINFONTSIZE     = 10
MINFONTPADDING  = 5
GRIDSPACING     = 4

# The hours range of the classes
FIRSTHOUR = dtime( 8, 0)
LASTHOUR  = dtime(18, 0)
CLASSHOURS = LASTHOUR.hour - FIRSTHOUR.hour + 1

# The days of classes
CLASSDAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

# Database Credentials
HOST     = "localhost"
PORT     = "5432"
DATABASE = "buap"
USER     = "postgres"
PASSWORD = "1234"

# | Auxiliar Functions |

# Used to use the colors with QColor function
def getQColor(rgb_string, alpha=255):
    # Example input: "rgb(150, 155, 165)"
    values = rgb_string.replace("rgb(", "").replace(")", "").split(",")
    r, g, b = map(int, values)
    return QColor(r, g, b, alpha)

# Used to get the optimal rows, cols of a certain n elements
def getRowsCols(n):
    if n == 0 : return 0, 0
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n/cols)
    return rows, cols

# | ----------------------------------------------------------------------- |

# | Course            | Internal representation of a schoolar class
class Course:
    def __init__(self, subject, teacher, hour, classType):
        self.subject   = subject
        self.teacher   = teacher # str
        self.hour      = hour    # datetime
        self.classType = classType

    def getDetails(self):
        return f"Curso de {self.subject} con {self.teacher} a las {self.hour} tipo: {self.classType}"

# | Classroom        | Internal representation of a class room
class Classroom:
    def __init__(self, name, capacity, building, floor, classType):
        self.name      = name
        self.capacity  = capacity
        self.building  = building
        self.floor     = floor
        self.classType = classType 
        self.schedule  = {d: {} for d in CLASSDAYS}

    # day : str(), hour : dtime(n, m), course: object
    def addCourse(self, day, hour, course):
        if FIRSTHOUR <= hour <= LASTHOUR:
            self.schedule[day][hour] = course

    # Return all the courses from a specific day
    def getDayCourses(self, day):
        return [course for course in self.schedule[day].values()]

    # Return all the courses from the week
    def getWeekCourses(self):
        courses = []
        for day in CLASSDAYS:
            courses.extend(self.getDayCourses(day))
        return courses

    def countCourses(self):
        return len(self.getWeekCourses())

    def occupiedPercentage(self):
        totalSpaces = CLASSHOURS * len(CLASSDAYS)
        occupiedSpaces = self.countCourses()
        if totalSpaces == 0:
            return 0  # avoid division by zero
        
        return (occupiedSpaces / totalSpaces) * 100

    def getDetails(self):
        txt = f"{self.building.name} : {self.name} ({self.capacity}) - Piso {self.floor} - Tipo de Salon {self.classType}\n"
        for d in CLASSDAYS:
            txt += f"        Clases del dia {d} -> \n"
            for course in self.schedule[d].values():
                txt += "       " + course.getDetails()
        return txt

# | Building         | Internal representation of a schoolar building
class Building:
    def __init__(self, name, area, classrooms=None):
        self.name = name
        self.area = area
        self.classrooms = classrooms if classrooms else []

    def addClassroom(self, classroom):
        self.classrooms.append(classroom)

    def getFloorClasrooms(self, floor):
        return [room for room in self.classrooms if room.floor == floor]

    def countClassrooms(self):
        return len(self.classrooms)

    def countFloorClassrooms(self, floor):
        return len(self.getFloorClassrooms(floor))

    def occupiedPercentajeByFloor(self, floor):
        floorClassrooms = self.getFloorClassrooms(floor)
        if not floorClassrooms: return 0
        return sum(room.occupiedPercentage() for room in floorClassrooms) / len(floorClassrooms)
    
    # Returns the average occupied percentage for the entire building
    def occupiedPercentage(self):
        if not self.classrooms: return 0
        return sum(room.occupiedPercentage() for room in self.classrooms) / len(self.classrooms)

    def getDetails(self):
        txt =  f"{self.name} - Area {self.area} \n Salones -> \n"
        for classroom in self.classrooms:
            txt += "       " + classroom.getDetails()
            
        return txt
    
# | Campus Data         | Data of the campus
class CampusData:
    def __init__(self, buildings):
        self.buildings = list(buildings.values())
        
        # Campus-level
        self.numCampusBuildings = 0
        self.numCampusClassrooms = 0
        self.numAreas = 0
        self.usedCampusSpaces = 0
        self.freeCampusSpaces = 0
        self.campusOccupancyPercentage = 0.0
        self.mostOccupiedCampusBuilding = None
        
        # Area-level
        self.areasInfo = {}
        
        # Building-level
        self.buildingsInfo = {}

        # Classroom-level
        self.classroomsInfo = {}
    
    def calculate(self):
        # - Campus Variables -
        
        self.numCampusBuildings = len(self.buildings)
        self.numCampusClassrooms = sum(len(b.classrooms) for b in self.buildings)
        self.numAreas = len(set(b.area for b in self.buildings))
        campusTotalSpaces = self.numCampusClassrooms * CLASSHOURS * len(CLASSDAYS)
        self.usedCampusSpaces = sum(c.countCourses() for b in self.buildings for c in b.classrooms)
        self.freeCampusSpaces = campusTotalSpaces - self.usedCampusSpaces
        self.campusOccupancyPercentage = (self.usedCampusSpaces / campusTotalSpaces) * 100 if campusTotalSpaces else 0
        self.mostOccupiedCampusBuilding = max(self.buildings, key=lambda b: b.occupiedPercentage())
        
        # - Area Variables
        for area in range(1, self.numAreas+1):
            areaBuildings = [b for b in self.buildings if b.area == area]
            areaClassrooms = [c for b in areaBuildings for c in b.classrooms]

            totalAreaSpaces = len(areaClassrooms) * CLASSHOURS * len(CLASSDAYS)
            usedAreaSpaces = sum(c.countCourses() for c in areaClassrooms)
            freeAreaSpaces = totalAreaSpaces - usedAreaSpaces
            occupancy = (usedAreaSpaces / totalAreaSpaces) * 100 if totalAreaSpaces else 0
            mostOccupied = max(areaBuildings, key=lambda b: b.occupiedPercentage())

            self.areasInfo[area] = {
                'numAreaBuildings': len(areaBuildings),
                'numAreaClassrooms': len(areaClassrooms),
                'usedAreaSpaces': usedAreaSpaces,
                'freeAreaSpaces': freeAreaSpaces,
                'areaOccupancyPercentage': occupancy,
                'mostOccupiedAreaBuilding': mostOccupied
            }
        
        # - Building Variables
        for build in self.buildings:
            buildingName = build.name
            classrooms   = build.classrooms
            
            # - Building Variables (all the building)
            numClassrooms = len(classrooms)
            numFloors = max((c.floor for c in classrooms)) 
            totalSpaces = numClassrooms * CLASSHOURS * len(CLASSDAYS)
            usedSpaces = sum(c.countCourses() for c in classrooms)
            freeSpaces = totalSpaces - usedSpaces
            occupancy = (usedSpaces / totalSpaces) * 100 if totalSpaces else 0
            mostOccupied = max(classrooms, key=lambda c: c.occupiedPercentage(), default=None)

            self.buildingsInfo[buildingName] = {
                'numBuildingClassrooms': numClassrooms,
                'numFloors': numFloors,
                'usedBuildingSpaces': usedSpaces,
                'freeBuildingSpaces': freeSpaces,
                'buildingOccupancyPercentage': occupancy,
                'mostOccupiedClassroom': mostOccupied
            }

            for floor in range(1, numFloors+1):
                floorClassrooms = [c for c in classrooms if c.floor == floor]
                totalFloorSpaces = len(floorClassrooms) * CLASSHOURS * len(CLASSDAYS)
                usedFloorSpaces = sum(c.countCourses() for c in floorClassrooms)
                freeFloorSpaces = totalFloorSpaces - usedFloorSpaces
                floorOccupancy = (usedFloorSpaces / totalFloorSpaces) * 100 if totalFloorSpaces else 0
                mostOccupiedFloorClassroom = max(floorClassrooms, key=lambda c: c.occupiedPercentage(), default=None)

                self.buildingsInfo[buildingName][floor] = {
                    'numFloorClassrooms': len(floorClassrooms),
                    'usedFloorSpaces': usedFloorSpaces,
                    'freeFloorSpaces': freeFloorSpaces,
                    'floorOccupancyPercentage': floorOccupancy,
                    'mostOccupiedClassroomOnFloor': mostOccupiedFloorClassroom
                }

                # - Classroom Variables (per room)
                for room in floorClassrooms:
                    totalClassroomSpaces = CLASSHOURS * len(CLASSDAYS)
                    courses = room.getWeekCourses()
                    usedClassroomSpaces = len(courses)
                    freeClassroomSpaces = totalClassroomSpaces - usedClassroomSpaces
                    classroomOcupancyPercentage = (usedClassroomSpaces / totalClassroomSpaces) * 100 if totalClassroomSpaces else 0
                    # Calcular % de coincidencia entre tipo de clase y tipo de salón
                    matchCount = sum(
                        1 for course in courses if hasattr(course, 'classType') and course.classType == room.classType
    )
                    subjectClassroomRelation = (matchCount / len(courses)) * 100 if courses else 0

                    self.buildingsInfo[buildingName][floor][room.name] = {
                        'usedClassroomSpaces': usedClassroomSpaces,
                        'freeClassroomSpaces': freeClassroomSpaces,
                        'classroomOcupancyPercentage': classroomOcupancyPercentage,
                        'subjectClassroomRelation': subjectClassroomRelation
                    }

                    for course in courses:
                        if hasattr(course, 'classType'):
                            courseType = course.classType
                            summary = self.buildingsInfo[buildingName][floor].setdefault(room.name, {}).setdefault('courseTypeSummary', {})
                            summary[courseType] = summary.get(courseType, 0) + 1

                    
                        
    def getCampusVariables(self):
        return {
            'numCampusBuildings': self.numCampusBuildings,
            'numCampusClassrooms': self.numCampusClassrooms,
            'numAreas': self.numAreas,
            'campusOccupancyPercentage': self.campusOccupancyPercentage,
            'mostOccupiedCampusBuilding': self.mostOccupiedCampusBuilding,
            'usedCampusSpaces': self.usedCampusSpaces,
            'freeCampusSpaces': self.freeCampusSpaces,
        }
    
    def getAreaVariables(self, area):
        return self.areasInfo[area]
    
    def getBuildingVariables(self, building):
        info = self.buildingsInfo[building.name]
        return {
            'numBuildingClassrooms': info['numBuildingClassrooms'],
            'numFloors': info['numFloors'],
            'usedBuildingSpaces': info['usedBuildingSpaces'],
            'freeBuildingSpaces': info['freeBuildingSpaces'],
            'buildingOccupancyPercentage': info['buildingOccupancyPercentage'],
            'mostOccupiedClassroom': info['mostOccupiedClassroom']
        }
    
    def getFloorBuildingVariables(self, building, floor):
        return self.buildingsInfo[building.name][floor]
    
    def getClassroomVariables(self, building, floor, classroom):
        return self.buildingsInfo[building.name][floor][classroom.name]
            
    def countBuildings(self):
        return len(self.buildings)

    def countAreaBuildings(self, area):
        return sum(1 for b in self.buildings if b.area == area)

    def countClassrooms(self):
        return sum(len(b.classrooms) for b in self.buildings)

    def countAreaClassrooms(self, area):
        return sum(len(b.classrooms) for b in self.buildings if b.area == area)
    
# | MainScreen       | The main screen of the program. Schedule is the csv file
class MainScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buildings = {}

        # Init of the retro font
        font         = QFontDatabase.addApplicationFont("fonts/vga437.ttf")
        self.vgaFont = QFontDatabase.applicationFontFamilies(font)[0]
        
        # Init of the right panel (info and stats)
        self.rightPanel = QLabel(self)
        self.rightPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.rightPanel.setWordWrap(True)
        self.rightPanel.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # Init of the left panel  (campus map)
        self.leftPanel = QWidget(self)
        self.leftPanel_layout = QVBoxLayout(self.leftPanel)
        self.gridPanel = QWidget(self.leftPanel) # Grid used to sort the elements on the campus map
        self.leftPanel_layout.addWidget(self.gridPanel)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fixUi()

    def fixUi(self):
        self.fixPanelSizes()
        self.fixPanelStyles()

    # Function who objective is update the sizes of the panels
    def fixPanelSizes(self):
        windowWidth  = self.width()
        windowHeight = self.height()
        
        # +-------------------------------------------------------+ 
        # |                                                    |__| <- (a) 
        # |  +------------------+       +----------------------+  |
        # |  |                  |       |                      |  |
        # |  |   Left Panel     |- (b) -|    Right Panel       |  |
        # |  |                  |       |                      |  |
        # |  +------------------+       +----------------------+  |
        # |        - (c) -                    - (d) -             | 
        # +-------------------------------------------------------+ 
        windowMarginProportion = 0.03  # (a)
        spacingProportion      = 0.04  # (b)
        leftWidthProportion    = 0.7   # (c)
        rightWidthProportion   = 0.2   # (d)

        newLeftWidth    = int(windowWidth  * leftWidthProportion)
        newRightWidth   = int(windowWidth  * rightWidthProportion)
        newHeight       = int(windowHeight * (1-windowMarginProportion * 2)) # Shared with both panels
        newWidthMargin  = int(windowWidth  * windowMarginProportion)
        newHeightMargin = int(windowHeight * windowMarginProportion)
        spacing = int(windowWidth * spacingProportion)

        self.leftPanel.setGeometry(newWidthMargin,
                                   newHeightMargin,
                                   newLeftWidth,
                                   newHeight)
        
        self.rightPanel.setGeometry(newWidthMargin + spacing + newLeftWidth,
                                    newHeightMargin,
                                    newRightWidth,
                                    newHeight)
        self.rightPanel.setFixedWidth(newRightWidth)
        self.rightPanel.setFixedHeight(newHeight)

    # Function who objective is update the style of the panels
    def fixPanelStyles(self):
        windowWidth  = self.width()
        windowHeight = self.height()

        # Get the new font size and padding
        newFontSize    = int(windowWidth / MINWINDOWWIDTH * MINFONTSIZE)
        newFontPadding = int(windowWidth / MINWINDOWWIDTH * MINFONTPADDING)
        
        # +---------+
        # |         |-+
        # |         | |
        # |  Panel  | |
        # |         | |
        # |         | |
        # +---------+ | <- Shadow
        #  +----------+
        xShadow = windowWidth  * 0.05 * 0.2 # <- HardCoded, it can improve 
        yShadow = windowHeight * 0.05 * 0.3

        panelStyle = f"""
        background-color: {COLORS['whitegrey']};
        color: {COLORS['darkblue']};        
        font-size: {newFontSize * 0.7}pt;
        padding: {newFontPadding}px;
        """

        # | RIGHT PANEL |

        # Right Shadow
        rightShadow = QGraphicsDropShadowEffect()
        rightShadow.setBlurRadius(0)
        rightShadow.setColor(getQColor(COLORS['darkblue']))
        rightShadow.setOffset(xShadow, yShadow)
        self.rightPanel.setGraphicsEffect(rightShadow)
        
        # Right Font
        self.rightPanel.setFont(QFont(self.vgaFont, newFontSize))

        # Right Style
        self.rightPanel.setStyleSheet(panelStyle)
        
        # | LEFT PANEL |
        
        # Left Shadow
        leftShadow = QGraphicsDropShadowEffect()
        leftShadow.setBlurRadius(0)
        leftShadow.setColor(getQColor(COLORS['darkblue']))
        leftShadow.setOffset(xShadow, yShadow)
        self.leftPanel.setGraphicsEffect(leftShadow)

        # Left Style
        self.leftPanel.setStyleSheet(panelStyle)

        # Tool type style
        QToolTip.setFont(QFont(self.vgaFont, int(newFontSize * 1)))
        
        # Style for every item in the panel (left)
        if self.gridPanel.layout():
            # Iterates for every item in the layout
            for i in range(self.gridPanel.layout().count()):
                widget = self.gridPanel.layout().itemAt(i).widget()
                
                if not widget: continue

                # With the widget name we set a custom style for every specific widget
                widgetName = widget.objectName()
                
                if   widgetName == "building":
                    percentage = widget.property("occupancyPercentage")
                    if   percentage > 60:
                        buildingColor = COLORS['darkblue']
                    elif percentage > 45:
                        buildingColor = COLORS['navyblue']
                    elif percentage > 30:
                        buildingColor = COLORS['blue']
                    elif percentage > 15:
                        buildingColor = COLORS['greyblue']
                    else:
                        buildingColor = COLORS['cyan']

                    widget.setFont(QFont(self.vgaFont, int(newFontSize * 1.8)))
                    widget.setStyleSheet(f"""
                    QPushButton{{
                    background-color : {buildingColor};
                    color: {COLORS['white']};
                    border-radius: 0px;
                    font-size: {int(newFontSize * 1.8)}pt;
                    text-align: center;
                    }}

                    QPushButton:hover {{
                    background-color: {COLORS['yellow']}; 
                    }}

                    QPushButton:pressed {{
                    background-color: {COLORS['red']};    
                    }}
                    
                    """)
                    buildingShadow = QGraphicsDropShadowEffect()
                    buildingShadow.setBlurRadius(0)
                    buildingShadow.setColor(getQColor(COLORS['grey']))
                    buildingShadow.setOffset(xShadow * 0.8, yShadow * 0.6)
                    widget.setGraphicsEffect(buildingShadow)
                        
                elif widgetName == "tableLabel":
                    widget.setFont(QFont(self.vgaFont, int(newFontSize * 1.2)))
                    widget.setStyleSheet(f"""
                    QLabel {{
                        background-color: {COLORS['darkblue']};
                        color: {COLORS['white']};
                        font-weight: bold;
                        font-size: {int(newFontSize * 1.2)}pt;
                        padding: 4px;
                    }}
                    """)
                    tableLabelShadow = QGraphicsDropShadowEffect()
                    tableLabelShadow.setBlurRadius(0)
                    tableLabelShadow.setColor(getQColor(COLORS['grey']))
                    tableLabelShadow.setOffset(xShadow * 0.2, yShadow * 0.2)
                    widget.setGraphicsEffect(tableLabelShadow)
                    pass
                
                elif widgetName == "tableField":
                    widget.setFont(QFont(self.vgaFont, int(newFontSize * 0.7)))
                    if widget.property("courseAssigned"):  # the color change if the class is assigned
                        tableFieldColor = COLORS['whitegrey']
                    else:
                        tableFieldColor = COLORS['white']
                    widget.setStyleSheet(f"""
                    QLabel {{
                        background-color: {tableFieldColor};
                        color: {COLORS['darkblue']};
                        font-size: {int(newFontSize * 0.7)}pt;
                    }}
                    
                    """)
                    tableFieldShadow = QGraphicsDropShadowEffect()
                    tableFieldShadow.setBlurRadius(0)
                    tableFieldShadow.setColor(getQColor(COLORS['grey']))
                    tableFieldShadow.setOffset(xShadow * 0.15, yShadow * 0.15)
                    widget.setGraphicsEffect(tableFieldShadow)
                
                elif widgetName == "title":
                    widget.setFont(QFont(self.vgaFont, int(newFontSize * 1.4)))
                    widget.setStyleSheet(f"""
                    background-color: {COLORS['navyblue']};
                    color: {COLORS['white']};
                    font-size: {int(newFontSize * 1.4)}pt;
                    padding: {int(newFontPadding * 1.5)}px;
                    """)
                    titleShadow = QGraphicsDropShadowEffect()
                    titleShadow.setBlurRadius(0)
                    titleShadow.setColor(getQColor(COLORS['grey']))
                    titleShadow.setOffset(xShadow * 0.8, yShadow * 0.6)
                    widget.setGraphicsEffect(titleShadow)
                elif widgetName == "button":
                    widget.setFont(QFont(self.vgaFont, int(newFontSize * 2)))
                    # Fix the tool tips used in the 'tableFields'
                    widget.setStyleSheet(f"""
                    QPushButton{{
                    background-color: {COLORS['navyblue']};
                    color: {COLORS['white']};
                    border-radius: 0px;
                    font-size: {int(newFontSize * 2)}pt;
                    }}
                    QPushButton:hover{{
                    background-color: {COLORS['yellow']};
                    }}
                    QPushButton:pressed{{
                    background-color: {COLORS['red']};
                    }}              
                    """)
                    buttonShadow = QGraphicsDropShadowEffect()
                    buttonShadow.setBlurRadius(0)
                    buttonShadow.setColor(getQColor(COLORS['grey']))
                    buttonShadow.setOffset(xShadow * 0.3, yShadow * 0.3)
                    widget.setGraphicsEffect(buttonShadow)
       
    def loadData(self, coursesList):
        # Connect to a postgres
        try:
            conn = psycopg2.connect(
                host=HOST,
                port=PORT,
                dbname=DATABASE,
                user=USER,
                password=PASSWORD
            )

            cursor = conn.cursor()

            # Extract the info about buildings and classrooms
            cursor.execute("""
            SELECT 
            e.nombre         AS edificio,
            a.id_aula,
            a.cupo,
            tc.nombre        AS tipo_clase
            FROM Aula a
            JOIN Edificio e     ON a.id_edificio = e.id_edificio
            JOIN Tipo_Clase tc  ON a.id_tipo_clase = tc.id_tipo_clase
            """)
            rows = cursor.fetchall()

            for row in rows:
                buildingName      = row[0]
                classroomName     = str(row[1])
                classroomCapacity = row[2]
                classroomType     = row[3]
                classroomFloor    = row[1] // 100
                
                if buildingName not in self.buildings:
                    self.buildings[buildingName] = Building(name=buildingName, area=1)

                classroom = Classroom(
                    name=classroomName,
                    capacity=classroomCapacity,
                    building=self.buildings[buildingName],
                    floor=classroomFloor,
                    classType=classroomType
                )

                self.buildings[buildingName].classrooms.append(classroom)

            # Using the schedule data complete the courses

            # Create mapping from subject name to class type
            cursor.execute("""
            SELECT 
            m.nombre AS materia,
            tc.nombre AS tipo_clase
            FROM Materia m
            JOIN Tipo_Clase tc ON m.id_tipo_clase = tc.id_tipo_clase
            """)
            rows = cursor.fetchall()
            
            # Store in a dictionary
            subjectTypeMap = {row[0]: row[1] for row in rows}
            
            for _, row in coursesList.iterrows():
                teacher     = row['Profesor']
                subject     = row['Materia']
                roomName    = str(int(row['Aula']))
                building    = str(row['Edificio'])
                day         = row['Día']
                strHour     = row['HoraInicio']
                subjectType = subjectTypeMap.get(subject)

                # Get the class type
                if not subjectType:
                    print(f"No class type found for subject: '{subject}'")
                    subjectType = "Sin definir"

                # Validate the day
                if day not in CLASSDAYS:
                    print(f"Skipping unknown day: '{day}'")
                    continue
                
                # Get the building object
                buildingObject = self.buildings.get(building)
                if not buildingObject:
                    print(f"Building '{building}' not found.")
                    continue

                
                # Get the classroom object from the building
                classroom = next((c for c in buildingObject.classrooms if c.name == roomName), None)
                if not classroom:
                    print(f"Classroom '{roomName}' not found in building '{building}'.")
                    continue

                # Transform the data
                hour, minute = map(int, strHour.split(":"))
                dtimeHour = dtime(hour, minute)

                # Create the course and add it to the classroom
                course = Course(subject=subject, teacher=teacher, hour=dtimeHour, classType=subjectType)
                
                classroom.addCourse(day=day, hour=dtimeHour, course=course)

            self.campusData = CampusData(self.buildings)
            self.campusData.calculate()
                
        except Exception as e:
            print("ERROR", e)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    def cleanGrid(self):
        oldGrid = self.gridPanel.layout()
        if oldGrid is not None:
            while oldGrid.count(): # While the grid have items
                widget = oldGrid.takeAt(0).widget()
                if widget is not None:
                    widget.setParent(None)
            QWidget().setLayout(oldGrid)

    def campusView(self, area=1):
        # | LEFT PANEL |
        
        self.cleanGrid()
        areaBuildings = [build for build in self.buildings.values() if build.area == area]
        gridRows, gridCols = getRowsCols(len(areaBuildings))

        # These are fixex values to get a better UI
        fixedRows = gridRows * 2
        fixedCols = gridCols * 2

        # We create the new grid
        grid = QGridLayout()
        grid.setSpacing(GRIDSPACING)

        # Title or Header
        title = QLabel(f"Benemerita Universidad Autonoma de Puebla - Campus Ciudad Universitaria 2 - Area {area}")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        grid.addWidget(title, 0, 0, 1, fixedCols+2)

        # Filler to keep the ahestetic
        fill = QLabel()
        fill.setStyleSheet("background-color: transparent; border: none;")
        grid.addWidget(fill, 1, 0, 1 , fixedCols+2)

        # Button to change the area
        totalAreas = self.campusData.getCampusVariables()['numAreas']
        if totalAreas > 1:
            if area < totalAreas:
                rightButton = QPushButton("->")
                rightButton.setObjectName("button")
                rightButton.clicked.connect(lambda: self.buildingView(building, area + 1))
                grid.addWidget(rightButton, fixedRows+2, fixedCols+1)
            elif area < 1:
                leftButton = QPushButton("<-")
                leftButton.setObjectName("button")
                leftButton.clicked.connect(lambda: self.buildingView(building, area - 1))
                grid.addWidget(leftButton, fixedRows+2, 0)
            else:
                rightFill = QLabel("")
                rightFill.setStyleSheet("background-color: transparent; border: none;")
                grid.addWidget(rightFill, fixedRows+2, 0, 1, fixedCols+2)
    
        # The buildings of the area
        # With the 2 first loops we go through all the grid with steps of 2
        # This because, our buildings are going to ocupy x2 of the normal size
        # While the index are going to iterate through the buildings
        idx = 0
        for row in range(0, fixedRows, 2):
            for col in range(0, fixedCols, 2):
                if idx < len(areaBuildings):
                    build = areaBuildings[idx]
                    occupancyPercentage = build.occupiedPercentage()
                    buildingButton = QPushButton(f"{build.name}\n{occupancyPercentage:.1f}%")
                    buildingButton.setProperty("occupancyPercentage", occupancyPercentage)
                    buildingButton.setObjectName("building")
                    buildingButton.clicked.connect(lambda checked, b=build: self.buildingView(b))
                    grid.addWidget(buildingButton, row + 2, col + 1, 2, 2)
                    idx += 1
        self.gridPanel.setLayout(grid)
                                                   
        # | RIGHT PANEL |
        
        # Extract all the info
        campusInfo = self.campusData.getCampusVariables()
        areaInfo   = self.campusData.getAreaVariables(area)
        text = textwrap.dedent(f"""\
        --------------------------                      
        INFORMACION DEL CAMPUS
        --------------------------
        Total de edificios: {campusInfo['numCampusBuildings']}
        Total de aulas: {campusInfo['numCampusClassrooms']}
        Total de áreas: {campusInfo['numAreas']}
        Ocupación promedio: {campusInfo['campusOccupancyPercentage']:.1f}%
        Edificio más ocupado: {campusInfo['mostOccupiedCampusBuilding'].name if campusInfo['mostOccupiedCampusBuilding'] else "N/A"}
        Espacios usados: {campusInfo['usedCampusSpaces']}
        Espacios sin usar: {campusInfo['freeCampusSpaces']}
        --------------------------
        INFORMACION DEL AREA {area}
        --------------------------
        Edificios en el área: {areaInfo['numAreaBuildings']}
        Aulas en el área: {areaInfo['numAreaClassrooms']}
        Ocupación promedio: {areaInfo['areaOccupancyPercentage']:.1f}%
        Edificio más ocupado: {areaInfo['mostOccupiedAreaBuilding'].name if areaInfo['mostOccupiedAreaBuilding'] else "N/A"}
        Espacios usados: {areaInfo['usedAreaSpaces']}
        Espacios sin usar: {areaInfo['freeAreaSpaces']}
        """)

        self.rightPanel.setText(text)

        self.fixUi()

    def buildingView(self, building, floor=1):
        # | LEFT PANEL |
        
        self.cleanGrid()

        buildingClassrooms = building.classrooms
        floorClassrooms    = [c for c in buildingClassrooms if c.floor == floor]
        totalFloors        = len((list(set(c.floor for c in buildingClassrooms))))
        gridRows, gridCols = getRowsCols(len(floorClassrooms))
                                                   
        # These are fixex values to get a better UI
        fixedRows = gridRows * 2
        fixedCols = gridCols * 2

        # We create the new grid
        grid = QGridLayout()
        grid.setSpacing(GRIDSPACING)

        # Title or Header
        title = QLabel(f"BUAP - CU2 - Edificio {building.name} - Piso {floor}")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        grid.addWidget(title, 0, 0, 1, fixedCols+2)

        # button to back to the campus view
        backCampusButton = QPushButton("x")
        backCampusButton.setObjectName("button")
        backCampusButton.clicked.connect(lambda: self.campusView(building.area))
        grid.addWidget(backCampusButton, 1, 0)                                        
    
        # Button to change the area
        if totalFloors > 1:
            if floor < totalFloors: # We need a button to go up
                upButton = QPushButton("+")
                upButton.setObjectName("button")
                upButton.clicked.connect(lambda: self.buildingView(building, floor+1))
                grid.addWidget(upButton, 1, fixedCols+1)
            else:                            # If not, we create a blank space to keep the ui good
                upFill = QLabel("")
                upFill.setStyleSheet("background-color: transparent; border: none;")
                grid.addWidget(upFill, 1, 1, 1, fixedCols+1)

            if floor > 1: # We need a button to go down
                downButton = QPushButton("-")
                downButton.setObjectName("button")
                downButton.clicked.connect(lambda: self.buildingView(building, floor-1))
                grid.addWidget(downButton, fixedRows+2, fixedCols+1)
            else:                            # If not, we create a blank space to keep the ui good
                downFill = QLabel("")
                downFill.setStyleSheet("background-color: transparent; border: none;")
                grid.addWidget(downFill, fixedRows+2, 0, 1, fixedCols+2)

        # The classrooms of the floor
        # With the 2 first loops we go through all the grid with steps of 2
        # This because, our buildings are going to ocupy x2 of the normal size
        # While the index are going to iterate through the classrooms
        idx = 0
        for row in range(0, fixedRows, 2):
            for col in range(0, fixedCols, 2):
                if idx < len(floorClassrooms):
                    room = floorClassrooms[idx]
                    occupancyPercentage = room.occupiedPercentage()
                    roomButton = QPushButton(f"{room.name}\n{occupancyPercentage:.1f}%")
                    roomButton.setProperty("occupancyPercentage", occupancyPercentage)
                    roomButton.setObjectName("building")
                    roomButton.clicked.connect(lambda checked, r=room: self.scheduleView(r))
                    grid.addWidget(roomButton, row+2, col+1, 2, 2)
                    idx += 1
        
        self.gridPanel.setLayout(grid)

        # | RIGHT PANEL |
        buildingInfo = self.campusData.getBuildingVariables(building)
        floorBuildingInfo = self.campusData.getFloorBuildingVariables(building, floor)

        # Calculate all the data
        text = textwrap.dedent(f"""\
        --------------------------
        INFORMACION DEL EDIFICIO
        --------------------------
        Nombre: {building.name}
        Area: {building.area}
        Número de aulas: {buildingInfo['numBuildingClassrooms']}
        Número de pisos: {buildingInfo['numFloors']}
        Ocupación promedio: {buildingInfo['buildingOccupancyPercentage']:.1f}%
        Aula más ocupada: {buildingInfo['mostOccupiedClassroom'].name if buildingInfo['mostOccupiedClassroom'] else "N/A"} 
        Bloques usados: {buildingInfo['usedBuildingSpaces']}
        Bloques sin usar: {buildingInfo['freeBuildingSpaces']}
        --------------------------
        INFORMACION DEL PISO {floor}
        --------------------------
        Aulas: {floorBuildingInfo['numFloorClassrooms']}
        Ocupación promedio: {floorBuildingInfo['floorOccupancyPercentage']:.1f}%
        Aula más ocupada: {floorBuildingInfo['mostOccupiedClassroomOnFloor'].name if floorBuildingInfo['mostOccupiedClassroomOnFloor'] else "N/A"}
        Bloques usados: {floorBuildingInfo['usedFloorSpaces']}
        Bloques sin usar: {floorBuildingInfo['freeFloorSpaces']}
        """)
        
        self.rightPanel.setText(text)

        self.fixUi()

    def scheduleView(self, classroom):
        # | LEFT PANEL |
        
        self.cleanGrid()
        gridRows = CLASSHOURS + 1 # +1 for the table labels
        gridCols = len(CLASSDAYS) + 1    # +2 for the table labels and the title

        # The grid
        grid = QGridLayout()
        grid.setSpacing(GRIDSPACING)

        # Title or header
        title = QLabel(f"BUAP - CU2 - Horario del {classroom.building.name} - {classroom.name}")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        grid.addWidget(title, 0, 0, 1, gridCols)

        # Button to get back to the building view
        backBuildingButton = QPushButton("x")
        backBuildingButton.setObjectName("button")
        backBuildingButton.clicked.connect(lambda: self.buildingView(classroom.building, classroom.floor))
        grid.addWidget(backBuildingButton, 1, 0)

        # Label for the class days
        for col, day in enumerate(CLASSDAYS):
            dayLabel = QLabel(day)
            dayLabel.setAlignment(Qt.AlignCenter)
            dayLabel.setObjectName("tableLabel")
            grid.addWidget(dayLabel, 1, col+1)

        # The hour and all the classes
        for row, hour in enumerate(range(FIRSTHOUR.hour, LASTHOUR.hour)):
            hourLabel = QLabel(f"{hour:02d}:00")
            hourLabel.setAlignment(Qt.AlignCenter)
            hourLabel.setObjectName("tableLabel")
            grid.addWidget(hourLabel, row+2, 0)

            # Actual content (courses or empty)
            for col, day in enumerate(CLASSDAYS):
                
                course = classroom.schedule.get(day, {}).get(dtime(hour, 0))
                
                courseLabel = QLabel()
                courseLabel.setMouseTracking(True)
                courseLabel.setWordWrap(True)

                if course:
                    courseLabel.setText(f"{course.subject}")
                    courseLabel.setProperty("courseAssigned", True)
                    courseLabel.setToolTip(f"Profesor: {course.teacher}\nTipo de Clase: {course.classType}")
                else:
                    courseLabel.setText("")
                    courseLabel.setProperty("courseAssigned", False)
                
                courseLabel.setAlignment(Qt.AlignCenter)
                courseLabel.setObjectName("tableField")
                grid.addWidget(courseLabel, row + 2, col + 1)

        self.gridPanel.setLayout(grid)
        
        # | RIGHT PANEL |

        classroomInfo   = self.campusData.getClassroomVariables(classroom.building, classroom.floor, classroom)

        courseTypes = classroomInfo.get('courseTypeSummary', {})
        #typeCoursesText = ""
        
            
        text = textwrap.dedent(f"""\
        --------------------------
        INFORMACION DEL SALON
        --------------------------
        Tipo de salón: {classroom.classType}
        Capacidad: {classroom.capacity} estudiantes
        Ocupación promedio: {classroomInfo['classroomOcupancyPercentage']:.1f}%
        Bloques usados: {classroomInfo['usedClassroomSpaces']}
        Bloques sin usar: {classroomInfo['freeClassroomSpaces']}
        --------------------------
        DESGLOSE POR TIPO DE CURSO
        --------------------------
        Aula adecuada promedio: {classroomInfo['subjectClassroomRelation']:.1f}%
        """)

        for courseType, value in courseTypes.items():
            text += f"{courseType} : {value}\n"
            
        self.rightPanel.setText(text)
        
        self.fixUi()

# | LoadData         | SubClass of QThread. His work is to load all the data
#                      that are we going to use in our MainScreen
class LoadData(QThread):
    finished = pyqtSignal()

    def __init__(self, mainScreen, filePath, parent=None):
        super().__init__(parent)
        self.mainScreen = mainScreen
        self.filePath   = filePath

    def run(self):
        self.mainScreen.loadData(self.filePath)
        self.finished.emit()

# | LoadingScreen    | SubClass of QLabel to simulate an sprite animation
class LoadingScreen(QLabel):
    def __init__(self, spritesPath, stepTimeMs=100, parent=None):
        super().__init__(parent)

        # Load the sprites
        self.idx = 0 # idx of the display
        self.sprites = []
        for file in sorted(os.listdir(spritesPath)):
            if file.endswith('.png'):
                img = QPixmap(os.path.join(spritesPath, file))
                self.sprites.append(img)

        self.setScaledContents(True)
        self.setVisible(False)

        # Setting the timer for the animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextFrame) # When the timer is over, it calls to nxt frame
        self.stepTime = stepTimeMs
        
        self.resize(self.parent().size())

    def resizeEvent(self, event):
        self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.fixBackground()
        super().resizeEvent(event)

    def start(self):
        if not self.sprites:
            return
        self.idx = 0
        self.fixBackground()
        self.setPixmap(self.sprites[self.idx])
        self.setVisible(True)
        self.raise_()
        self.resize(self.parent().size())
        self.timer.start(self.stepTime)

    def stop(self):
        self.timer.stop()
        self.setVisible(False)
        self.clear()

    def nextFrame(self):
        self.idx = (self.idx + 1) % len(self.sprites)
        self.fixBackground()

    def fixBackground(self):
        if not self.sprites:
            return
        
        originalSprite = self.sprites[self.idx]
        scaledSprite   = originalSprite.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.FastTransformation
        )
        self.setPixmap(scaledSprite)
        
# | SpriteButton     | SubClass of QLabel to simulate a sprite (hover, press)
class SpriteButton(QLabel):
    clic = pyqtSignal()

    def __init__(self, spriteBase, spriteHover, spriteClick, parent=None):
        super().__init__(parent)

        # Setting the sprites
        self.pixmapBase  = QPixmap(spriteBase)
        self.pixmapHover = QPixmap(spriteHover)
        self.pixmapClick = QPixmap(spriteClick)

        self.setPixmap(self.pixmapBase) # Set the default sprite
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMouseTracking(True)     # Allows hover

        self.isClicked = False

    # Detects when the mouse is above the button
    def enterEvent(self, event):
        if not self.isClicked:
            self.setPixmap(self.pixmapHover)

    # Detects when the mouse is not above the button
    def leaveEvent(self, event):
        if not self.isClicked:
            self.setPixmap(self.pixmapBase)

    # Detects when the mouse is being press
    def mousePressEvent(self, event):
        self.isClicked = True
        self.setPixmap(self.pixmapClick)
        super().mousePressEvent(event) # Calls the parent mousePressEvent

    # Detects when the mouse is not being press anymore
    def mouseReleaseEvent(self, event):
        self.isClicked = False
        if self.rect().contains(event.pos()): # If the mouse is still above the button
            self.setPixmap(self.pixmapHover)
            self.clic.emit()
        else:
            self.setPixmap(self.pixmapBase)
        super().mouseReleaseEvent(event)

# | MainWindow       |

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PLANIFICACIÓN HORARIOS - BUAP CU2")
        self.setMinimumSize(MINWINDOWWIDTH, MINWINDOWHEIGHT)

        # Load the background image
        self.backgroundImagePath = 'imgs/pantallaInicio.png'
        self.backgroundImage = QLabel(self)
        self.backgroundImage.setScaledContents(False)
        self.backgroundImage.lower()

        # Load the 'load csv' button
        self.baseButtonPath  = 'imgs/botonCsvNomal.png'
        self.hoverButtonPath = 'imgs/botonCsvHover.png'
        self.clickButtonPath = 'imgs/botonCsvClick.png'
        self.csvButton = SpriteButton(self.baseButtonPath, self.hoverButtonPath, self.clickButtonPath)
        self.csvButton.setParent(self)
        self.csvButton.clic.connect(self.loadCsv)

        # Load the loading screen
        loadingScreenAnimationPath = 'imgs/pantallaCarga'
        self.loadingScreen = LoadingScreen(loadingScreenAnimationPath, parent=self)
        
        # Load the main screen
        self.mainScreen = MainScreen()
        self.setCentralWidget(self.mainScreen)
        self.mainScreen.hide()

        self.fixUi()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fixUi()
        self.loadingScreen.resize(self.size())
        
    def fixUi(self):
        self.fixBackground()
        self.fixButton()

    def fixBackground(self):
        img  = QPixmap(self.backgroundImagePath)
        if not img.isNull():
            scaledImg = img.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.FastTransformation
            )
            self.backgroundImage.setPixmap(scaledImg)
            self.backgroundImage.setGeometry(0, 0, self.width(), self.height())
    
    def fixButton(self):
        windowWidth  = self.width()
        windowHeight = self.height()

        # Calculate the apropiate scaling factor
        widthFactor  = windowWidth  / MINWINDOWWIDTH
        heightFactor = windowHeight / MINWINDOWHEIGHT
        scaleFactor  = min(widthFactor, heightFactor)

        newButtonWidth  = max(MINBUTTONWIDTH,  int(MINBUTTONWIDTH  * scaleFactor))
        newButtonHeight = max(MINBUTTONHEIGHT, int(MINBUTTONHEIGHT * scaleFactor))
        newMargin = int(MINWINDOWMARGIN * scaleFactor)
        
        self.csvButton.pixmapBase = self.csvButton.pixmapBase.scaled(
            newButtonWidth, newButtonHeight, Qt.KeepAspectRatioByExpanding, Qt.FastTransformation
        )
        self.csvButton.pixmapHover = self.csvButton.pixmapHover.scaled(
            newButtonWidth, newButtonHeight, Qt.KeepAspectRatioByExpanding, Qt.FastTransformation
        )
        self.csvButton.pixmapClick = self.csvButton.pixmapClick.scaled(
            newButtonWidth, newButtonHeight, Qt.KeepAspectRatioByExpanding, Qt.FastTransformation
        )

        self.csvButton.setPixmap(self.csvButton.pixmapBase)
        
        xPos = windowWidth  - newButtonWidth  - newMargin
        yPos = windowHeight - newButtonHeight - newMargin
        
        self.csvButton.setGeometry(xPos, yPos, newButtonWidth, newButtonHeight)
        
    def loadCsv(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "Selecciona tu archivo CSV",
            "",
            "Archivos CSV (*.csv);;Todos los archivos (*)"
        )
        if filePath:
            csv = pd.read_csv(filePath)

            if self.checkCsv(csv):
                print("Archivo bien")
                # Provisional
                #csv.dropna(inplace=True)
                # Iniciar Pantalla de Carga
                self.startLoadingScreen(csv)
            else:
                print("Archivo mal")
                # Tirar algún tipo de error

    def checkCsv(self, csv):
        required_columns = [
        "Profesor", "Materia", "Aula", "Edificio", "Día", 
        "HoraInicio", "HoraFin", "HoraNum", "DiaNum", "AulaCompleta"
        ]

        # 1. Check if all required columns are present
        if not all(col in csv.columns for col in required_columns): return False

        # 2. Check for missing values in required columns
        if csv[required_columns].isnull().any().any(): return False

        return True
    
    def startLoadingScreen(self, filePath):
        # Hide the actual elements
        self.csvButton.hide()
        self.backgroundImage.hide()

        self.loadingScreen.start()

        # Start the work
        self.work = LoadData(self.mainScreen, filePath)
        self.work.finished.connect(self.stopLoadingScreen)
        self.work.start()

    def stopLoadingScreen(self):
        self.loadingScreen.stop()
        # Change the window color
        self.setStyleSheet(f"background-color: {COLORS['cyan']};") # Color gris
        self.mainScreen.campusView()
        self.mainScreen.show()
        self.mainScreen.raise_()
        
# | Main             |

def main():
    app = QApplication(sys.argv)

    # For some reason you have to define QToolTip as global lol
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setStyleSheet(f"""
    QToolTip {{
    background-color: {COLORS['darkblue']}; 
    color: {COLORS['darkblue']}; 
    border-radius: 0px;
    }}""")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# | ----------------------------------------------------------------------- |
