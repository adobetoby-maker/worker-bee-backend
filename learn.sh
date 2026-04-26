#!/bin/zsh
cd ~/worker-bee
source .venv/bin/activate
export OLLAMA_HOST=http://localhost:11434
python3 -c "
import asyncio
from agent.tools.memory import MemoryTool
from agent.tools.learner import learn_session
memory = MemoryTool(tab_id='auto-learner')
asyncio.run(learn_session(memory=memory))
"
echo "Learning session complete: $(date)"
