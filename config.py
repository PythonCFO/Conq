gameID = "uuid"
world = {}
regions = {}
territories = {}
users = {}
players = {}   #This should include sharable data: name, stats, card qty, etc.
cards = {}
stage = {'Setup', 'Play', 'Victory', 'Draw'}
turn = {}   #Include round, player, phase

send_queues = {}
recv_queue = ""

DEBUG = False
VERBOSE = True


classic_territories = [
    ['North America', 'Alaska', ['Northwest Territory', 'Alberta', 'Kamchatka']],
    ['North America', 'Alberta', ['Alaska', 'Northwest Territory', 'Ontario', 'Western United States']],
    ['North America', 'Central America', ['Western United States', 'Eastern United States', 'Venezuela']],
    ['North America', 'Eastern United States', ['Central America', 'Western United States', 'Quebec', 'Ontario']],
    ['North America', 'Greenland', ['Iceland', 'Northwest Territory', 'Ontario', 'Quebec']],
    ['North America', 'Northwest Territory', ['Alaska', 'Greenland', 'Ontario', 'Alberta']],
    ['North America', 'Ontario', ['Alberta', 'Northwest Territory', 'Greenland', 'Quebec', 'Eastern United States', 'Western United States']],
    ['North America', 'Quebec', ['Ontario', 'Greenland', 'Eastern United States']],
    ['North America', 'Western United States', ['Alberta', 'Ontario', 'Eastern United States', 'Central America']],
    ['South America', 'Argentina', ['Peru', 'Brazil']],
    ['South America', 'Brazil', ['Peru', 'Venezuela', 'Argentina']],
    ['South America', 'Peru', ['Venezuela', 'Brazil', 'Argentina']],
    ['South America', 'Venezuela', ['Brazil', 'Peru', 'Central America']],
    ['Europe', 'Great Britain', ['Iceland', 'Scandinavia', 'Northern Europe', 'Western Europe']],
    ['Europe', 'Iceland', ['Greenland', 'Great Britain', 'Scandinavia']],
    ['Europe', 'Northern Europe', ['Great Britain', 'Scandinavia', 'Ukraine', 'Southern Europe', 'Western Europe']],
    ['Europe', 'Scandinavia', ['Iceland', 'Ukraine', 'Northern Europe', 'Great Britain']],
    ['Europe', 'Southern Europe', ['Western Europe', 'Northern Europe', 'Ukraine', 'Middle East', 'Egypt', 'North Africa']],
    ['Europe', 'Ukraine', ['Northern Europe', 'Scandinavia', 'Ural', 'Afghanistan', 'Middle East', 'Southern Europe']],
    ['Europe', 'Western Europe', ['Great Britain', 'Northern Europe', 'Southern Europe', 'North Africa']],
    ['Africa', 'Congo', ['North Africa', 'East Africa', 'South Africa']],
    ['Africa', 'East Africa', ['Congo', 'North Africa', 'Egypt', 'Middle East', 'Madagascar', 'South Africa']],    
    ['Africa', 'Egypt', ['North Africa', 'Southern Europe', 'Middle East', 'East Africa']],
    ['Africa', 'Madagascar', ['East Africa', 'South Africa']],
    ['Africa', 'North Africa', ['Western Europe', 'Southern Europe', 'Egypt', 'East Africa', 'Congo', 'Brazil']],
    ['Africa', 'South Africa', ['Congo', 'East Africa', 'Madagascar']],
    ['Asia', 'Afghanistan', ['Middle East', 'Ukraine', 'Ural', 'China', 'India']],
    ['Asia', 'China', ['India', 'Afghanistan', 'Ural', 'Siberia', 'Mongolia', 'Siam']],
    ['Asia', 'India', ['Middle East', 'Afghanistan', 'China', 'Siam']],
    ['Asia', 'Irkutsk', ['Siberia', 'Yakutsk', 'Kamchatka', 'Mongolia']],
    ['Asia', 'Japan', ['Mongolia', 'Kamchatka']],
    ['Asia', 'Kamchatka', ['Mongolia', 'Irkutsk', 'Yakutsk', 'Alaska', 'Japan']],
    ['Asia', 'Middle East', ['Egypt', 'Southern Europe', 'Ukraine', 'Afghanistan', 'India', 'East Africa']],
    ['Asia', 'Mongolia', ['China', 'Siberia', 'Irkutsk', 'Kamchatka', 'Japan']],
    ['Asia', 'Siam', ['India', 'China', 'Indonesia']],
    ['Asia', 'Siberia', ['Ural', 'Yakutsk', 'Irkutsk', 'Mongolia', 'China']],
    ['Asia', 'Ural', ['Ukraine', 'Siberia', 'China', 'Afghanistan']],
    ['Asia', 'Yakutsk', ['Siberia', 'Kamchatka', 'Irkutsk']],
    ['Australia', 'Eastern Australia', ['Western Australia', 'New Guinea']],
    ['Australia', 'Indonesia', ['Siam', 'New Guinea', 'Western Australia']],
    ['Australia', 'New Guinea', ['Indonesia', 'Eastern Australia', 'Western Australia']],
    ['Australia', 'Western Australia', ['Indonesia', 'New Guinea', 'Eastern Australia']]
]

region_bonus = {'North America':5, 'South America':2, 'Europe':5, 'Africa':3, 'Asia':7, 'Australia':2}

classic_cards = [
    ['Alaska', 'Cavalry'],
    ['Alberta', 'Artillery'],
    ['Central America', 'Cavalry'],
    ['Eastern United States', 'Artillery'],
    ['Greenland', 'Infantry'],
    ['Northwest Territory', 'Cavalry'],
    ['Ontario', 'Cavalry'],
    ['Quebec', 'Artillery'],
    ['Western United States', 'Cavalry'],
    ['Argentina', 'Cavalry'],
    ['Brazil', 'Cavalry'],
    ['Peru', 'Cavalry'],
    ['Venezuela', 'Cavalry'],
    ['Great Britain', 'Cavalry'],
    ['Iceland', 'Infantry'],
    ['Northern Europe', 'Infantry'],
    ['Scandinavia', 'Cavalry'],
    ['Southern Europe', 'Cavalry'],
    ['Ukraine', 'Infantry'],
    ['Western Europe', 'Infantry'],
    ['Congo', 'Cavalry'],
    ['East Africa', 'Artillery'],
    ['Egypt', 'Infantry'],
    ['Madagascar', 'Cavalry'],
    ['North Africa', 'Infantry'],
    ['South Africa', 'Infantry'],
    ['Afghanistan', 'Cavalry'],
    ['China', 'Infantry'],
    ['India', 'Cavalry'],
    ['Irkutsk', 'Artillery'],
    ['Japan', 'Cavalry'],
    ['Kamchatka', 'Artillery'],
    ['Middle East', 'Infantry'],
    ['Mongolia', 'Artillery'],
    ['Siam', 'Infantry'],
    ['Siberia', 'Artillery'],
    ['Ural', 'Infantry'],
    ['Yakutsk', 'Cavalry'],
    ['Eastern Australia', 'Artillery'],
    ['Indonesia', 'Artillery'],
    ['New Guinea', 'Infantry'],
    ['Western Australia', 'Cavalry'],
    ['Wild_1', 'All'],  # Need unique name
    ['Wild_2', 'All']   # Need unique name
]

game_players = [('Andrew', 'Blue'), 
           ('Jay', 'Red'),
           ('Frank', 'Green'),
           ('Becky', 'Pink')
]

classic_army_center = {
    'Argentina': (194.4, 405.8),
    'Peru': (188.1, 346.9),
    'Brazil': (236.3, 325.1),
    'Venezuela': (177.6, 280.6),
    'Central America': (125.2, 236.9),
    'Western United States': (118.6, 175.6),
    'Eastern United States': (176.3, 189.4),
    'Alberta': (116.3, 122.9),
    'Ontario': (164.8, 131.7),
    'Quebec': (216.9, 130.7),
    'Alaska': (56., 82.9),
    'Northwest Territory': (126.2, 81.6),
    'Greenland': (261.2, 53.4),
    'Iceland': (320.8, 105.8),
    'Great Britain': (306.7, 165.2),
    'Scandinavia': (368., 112.1),
    'Northern Europe': (374.9, 171.7),
    'Western Europe': (315.9, 238.6),
    'Southern Europe': (382.7, 214.3),
    'Ukraine': (445., 133.7),
    'North Africa': (346.4, 309.7),
    'Egypt': (403., 288.4),
    'East Africa': (436.5, 340.1),
    'Congo': (404., 374.9),
    'South Africa': (411.9, 439.4),
    'Madagascar': (473.2, 444.7),
    'Middle East': (458.1, 261.5),
    'Afghanistan': (503.3, 194.3),
    'Ural': (514.1, 127.1),
    'Siberia': (548.2, 86.8),
    'Yakutsk': (608.2, 71.8),
    'Irkutsk': (597.4, 136.),
    'Mongolia': (609.5, 178.6),
    'Kamchatka': (663.9, 74.4),
    'Japan': (681.2, 186.1),
    'China': (597., 224.1),
    'Middle East': (459.4, 255.9),
    'India': (542.6, 260.8),
    'Siam': (600.3, 284.1),
    'Indonesia': (624.6, 362.4),
    'New Guinea': (678.3, 346.),
    'Eastern Australia': (691.7, 414.8),
    'Western Australia': (640.6, 440.1)
}