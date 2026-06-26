from app.api.chat import event_generator

msgs = [{"role": "user", "content": "What time is it in UTC?"}]

print("Running event_generator for test prompt:\n")
for e in event_generator(msgs):
    print(repr(e))
