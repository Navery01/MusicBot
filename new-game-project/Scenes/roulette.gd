extends Node2D

@onready var WHEEL = $Wheel
# Called when the node enters the scene tree for the first time.

@onready var waiting = true
@onready var spin_timer = $SpinTimer
@onready var wait_timer = $DelayTimer
@onready var chip = preload("res://Scenes/chip.tscn")


var bet_positions

func _ready() -> void:
	WHEEL.spin_timer = spin_timer
	wait_timer.start()
	wait_timer.connect("timeout", _on_wait_timer_timeout)
	spin_timer.connect("timeout", _on_spin_timer_timeout)
	bet_positions = get_tree().get_nodes_in_group("RouletteBet")
	
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	$Label.text = 'Time Left: %d' % spin_timer.time_left
	$Label2.text = 'Next Spin In: %d' % wait_timer.time_left
	WHEEL.get_current_index()

func _on_spin_timer_timeout():
	wait_timer.start()
	$SpinBox.editable = true
	print("Wheel Rotation: %d" % WHEEL.rotation_deg)
	print("Wheel Index: %s" % WHEEL.get_current_index()[0])
	print("Wheel color: %s" % WHEEL.get_current_index()[1])
	
	
	await wipe_chips()

func _on_wait_timer_timeout():
	randomize()
	lock_in_bet()
	#print('Betting:%2d' % bet_amt)
	#print('Selection: %s' %bet_color)
	spin_timer.wait_time = randf_range(3.0, 15.0)
	spin_timer.start()
	WHEEL.reset_wheel()
	WHEEL.is_spinning = true
	
func lock_in_bet():
	$SpinBox.apply()
	$SpinBox.editable = false
	

func wipe_chips():
	randomize()
	for chip:Area2D in get_tree().get_nodes_in_group("Chip"):
		var area; 
		for obj in chip.get_overlapping_areas(): 
			if obj.is_in_group("RouletteBet"):
				area = obj
		if area.is_in_group("RouletteBet"):
			if area.get_value() == WHEEL.get_current_index()[0]:
				for x in (1.0 / area.get_odds()) - 1:
					var new_chip = create_chip(area.position)
					new_chip.retract($award.position)
				chip.retract($award.position)
			elif area.get_value() == WHEEL.get_current_index()[1]:
				for x in (1.0 / area.get_odds()) - 1:
					var new_chip = create_chip(area.position)
					new_chip.retract($award.position)
				chip.retract($award.position)
				
			else:
				chip.queue_free()
	$SpinBox.value = 0

func get_balance():
	var bal = 0
	var chips = get_tree().get_nodes_in_group("Chip")
	for chip in chips:
		bal += chip.value

	return bal
		
func create_chip(pos:Vector2):
	var playerchip = chip.instantiate()
	get_tree().root.add_child(playerchip)
	playerchip.position = pos
	playerchip.add_to_group("Chip")
	return playerchip


func _on_spin_box_value_changed(value: float) -> void:
	if value  > 0:
		var new_chip = create_chip($award.position)
		new_chip.get_node("Sprite2D").position = Vector2(0, (int(value) / 25) * -5)
