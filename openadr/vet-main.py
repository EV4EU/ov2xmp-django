from openleadr import OpenADRClient
import asyncio


async def main():
    client = OpenADRClient(ven_name="ov2xmp",
                           vtn_url="http://localhost:8080/OpenADR2/Simple/2.0b")
    client.add_handler('on_event', handle_event)
    await client.run()


async def handle_event(event):
    """
    This coroutine will be called
    when there is an event to be handled.
    """
    print("There is an event!")
    print(event)
    # Do something to determine whether to Opt In or Opt Out
    return 'optIn'


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()



