import asyncio
import sys
asyncio.set_event_loop(asyncio.new_event_loop())
sys.argv = [
    'snmpsim-command-responder',
    '--data-dir=/app/data',
    '--agent-udpv4-endpoint=0.0.0.0:11611',
    '--process-user=nobody',
    '--process-group=nogroup'
]
from snmpsim.commands.responder import main
main()
