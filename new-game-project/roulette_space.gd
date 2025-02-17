extends Area2D

var SPACE_VALUE:int
var ODDS:float = 1/35

# Called when the node enters the scene tree for the first time.

func get_odds():
	return ODDS
	
func get_value():
	return SPACE_VALUE
	

func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
