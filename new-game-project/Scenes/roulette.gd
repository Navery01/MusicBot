extends Node2D

@onready var WHEEL = $Wheel
# Called when the node enters the scene tree for the first time.

@onready var waiting = true
@onready var spin_timer = $SpinTimer
@onready var wait_timer = $DelayTimer


func _ready() -> void:
	WHEEL.spin_timer = spin_timer
	wait_timer.start()
	wait_timer.connect("timeout", _on_wait_timer_timeout)
	spin_timer.connect("timeout", _on_spin_timer_timeout)
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	$Label.text = 'Time Left: %d' % spin_timer.time_left
	$Label2.text = 'Next Spin In: %d' % wait_timer.time_left
	

func _on_spin_timer_timeout():
	wait_timer.start()
	print("Wheel Rotation: %d" % WHEEL.rotation_deg)
	print("Wheel Index: %s" % WHEEL.get_current_index()[0])
	print("Wheel color: %s" % WHEEL.get_current_index()[1])
	

func _on_wait_timer_timeout():
	randomize()
	spin_timer.wait_time = randf_range(3.0, 15.0)
	spin_timer.start()
	WHEEL.reset_wheel()
	WHEEL.is_spinning = true
