extends Area2D

var drop_spots
var is_dragging = false
var mouse_offset
var delay = 0.2
var owner_id = '1234'
var value = 25
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	drop_spots = get_tree().get_nodes_in_group("RouletteBet")
	


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if is_dragging == true:
		var tween = get_tree().create_tween()
		tween.tween_property(self, "position", get_global_mouse_position() - mouse_offset, delay * delta)


func _on_input_event(viewport: Node, event: InputEvent, shape_idx: int) -> void:
	if event is InputEventMouseButton and event.button_index == 1:
		if event.is_pressed():
			if get_viewport_rect().has_point(event.position):
				is_dragging = true
				mouse_offset = get_global_mouse_position() - global_position
		else:
			is_dragging = false
			for drop_spot in drop_spots:
				if drop_spot.has_overlapping_areas() and drop_spot.get_overlapping_areas().has(self):
					var snap_pos = drop_spot.position + Vector2(randi() % 15, randi() % 15)
					var tween = get_tree().create_tween()
					tween.tween_property(self, "position", snap_pos, delay)

func retract(position: Vector2):
	var tween = get_tree().create_tween()
	tween.tween_property(self, "position", position, delay)
