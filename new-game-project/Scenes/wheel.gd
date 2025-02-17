extends Sprite2D

const positions = ['0', '28', '9', '26', '30', '11', '7', '20', '32', '17', '5', '22', '34', '15', '3', '24'
, '36', '13', '1', '00', '27', '10', '25', '29','12', '8', '19', '31', '18', '6', '21', '33', '16', '4', '23', '35', '14', '2']
var black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
var red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

const spin_speed = 5
var spin_timer:Timer
var is_spinning

var rotation_deg = 0
var current_index = positions[0]

var textures = {
	'base':load("res://Assets/wheel_pos/base.png")\
	, '00':load("res://Assets/wheel_pos/pos_00.png")
}


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	is_spinning = false
	for i in range(37):
		textures['%d' % i] = load("res://Assets/wheel_pos/pos_%d.png" % i)

	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if is_spinning:
		start_spinning(delta)
	
func start_spinning(delta):
	if not spin_timer.is_stopped():
		rotation += spin_speed * spin_timer.time_left * delta
		rotation_deg = rotation * (180/PI)
		
func reset_wheel():
	rotation = 0
	
func get_current_index():
	current_index = positions[-round((int(rotation_deg) % 360)/ 9.47368421053)]
	flicker_position(int(current_index))
	var color
	if int(current_index) in black_numbers:
		color = 'black'
	elif int(current_index) in red_numbers:
		color = 'red'
	else:
		color = 'green'
	return [current_index, color]
	
func flicker_position(idx):
	texture = textures['%d' % idx]
