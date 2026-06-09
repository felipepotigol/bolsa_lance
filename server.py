import flwr as fl

strategy = fl.server.strategy.FedAvg()

fl.server.start_server(
    server_address="0.0.0.0:8081",
    strategy=strategy,
    config=fl.server.ServerConfig(num_rounds=3)
)