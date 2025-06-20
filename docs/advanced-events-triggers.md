# 🔁 Event and Trigger System

## How Events Are Triggered
Events are triggered by entering map areas, interacting with objects, or performing specific actions. For example, entering a certain tile or colliding with an NPC can start a dialogue or quest.

### Example
"When entering the forest, if the player has the golden key, the Old Man NPC appears."

## Time- or Action-Based Triggers
- Quest scheduling
- Weather changes (rain, wind, leaves)
- Enemy respawn and boss events
- Cutscenes and dialogues

The system uses periodic checks and state machines (FSMs) to control event flow. See `level.py` and `npc.py` for implementation details.

---
