extends Control

@export var address = "127.0.0.1"
@export var port = 8910

var peer
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	multiplayer.peer_connected.connect(player_connected)
	multiplayer.peer_disconnected.connect(player_disconnected)
	multiplayer.connected_to_server.connect(connected_to_server)
	multiplayer.connection_failed.connect(connection_failed)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_join_roulette_button_down() -> void:
	peer = ENetMultiplayerPeer.new()
	peer.create_client(address, port)
	peer.get_host().compress(ENetConnection.COMPRESS_RANGE_CODER)
	multiplayer.set_multiplayer_peer(peer)
	
func _on_host_roulette_pressed() -> void:
	peer = ENetMultiplayerPeer.new()
	var error = peer.create_server(port, 4)
	if error != OK:
		print("cannot host:" + str(error))
		return
	peer.get_host().compress(ENetConnection.COMPRESS_RANGE_CODER)
	
	multiplayer.set_multiplayer_peer(peer)
	print("waiting for players...")


func _on_start_lobby_pressed() -> void:
	pass # Replace with function body.
	

func connected_to_server():
	print("Connected To Server")
	
func connection_failed():
	print("Connection Failed")
	
func player_connected(id):
	print("Player Connected: %s" %str(id))
	
func player_disconnected(id):
	print("Player Disconnected: %s" %str(id))
