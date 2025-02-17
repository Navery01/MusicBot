extends Sprite2D

var spin_timer
var wait_timer

const positions = ['0', '28', '9', '26', '30', '11', '7', '20', '32', '17', '5', '22', '34', '15', '3', '24'
, '36', '13', '1', '00', '27', '10', '25', '29','12', '8', '19', '31', '18', '6', '21', '33', '16', '4', '23', '35', '14', '2']
var black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
var red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func get_space():
	return positions[randi() % 38]
