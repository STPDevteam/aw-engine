from global_methods import *

import datetime
import json
import sys


class Scratch:
    def get_from_db(self, key, default=None):
        if self.memory.check_key(self.key_pattern + key):
            return self.memory.get_key_otherwise_return_defalut(
                self.key_pattern + key, default
            )
        else:
            return default

    def __init__(self, persona_name, memory):
        self.memory = memory
        self.key_pattern = f"Scratch:{persona_name}:"
        self.vision_r = self.get_from_db(self.key_pattern + "vision_r", 4)
        self.att_bandwidth = self.get_from_db(self.key_pattern + "att_bandwidth", 3)
        self.retention = self.get_from_db(self.key_pattern + "retention", 5)

        # WORLD INFORMATION
        # Perceived world time.
        self.step = self.get_from_db("step", 0)
        self.start_step = self.get_from_db("start_step", 0)
        self.time_per_step = self.get_from_db("time_per_step", 10)
        # curr_minute = (self.start_step + self.step) * self.time_per_step
        # curr_time_delta = datetime.timedelta(minutes=curr_minute)
        # epoch_time = datetime.datetime(2024, 4, 9)
        # curr_time = epoch_time + curr_time_delta
        self.curr_time = self.from_step_to_time(self.step)
        # Current x,y tile coordinate of the persona.
        self.curr_tile = self.get_from_db("curr_tile")
        # Perceived world daily requirement.
        self.daily_plan_req = self.get_from_db("daily_plan_req")

        # THE CORE IDENTITY OF THE PERSONA
        # Base information about the persona.
        self.name = self.get_from_db("name")
        self.first_name = self.get_from_db("first_name")
        self.last_name = self.get_from_db("last_name")
        self.age = self.get_from_db("age")
        # L0 permanent core traits.
        self.innate = self.get_from_db("innate")
        # L1 stable traits.
        self.learned = self.get_from_db("learned")
        # L2 external implementation.
        self.currently = self.get_from_db("currently")
        self.lifestyle = self.get_from_db("lifestyle")
        self.living_area = self.get_from_db("living_area")

        # REFLECTION VARIABLES
        self.concept_forget = self.get_from_db("concept_forget", 100)
        self.daily_reflection_time = self.get_from_db("daily_reflection_time", 60 * 3)
        self.daily_reflection_size = self.get_from_db("daily_reflection_size", 5)
        self.overlap_reflect_th = self.get_from_db("overlap_reflect_th", 2)
        self.kw_strg_event_reflect_th = self.get_from_db("kw_strg_event_reflect_th", 4)
        self.kw_strg_thought_reflect_th = self.get_from_db(
            "kw_strg_thought_reflect_th", 4
        )
        # New reflection variables
        self.recency_w = self.get_from_db("recency_w", 1)
        self.relevance_w = self.get_from_db("relevance_w", 1)
        self.importance_w = self.get_from_db("importance_w", 1)
        self.recency_decay = self.get_from_db("recency_decay", 0.99)
        self.importance_trigger_max = self.get_from_db("importance_trigger_max", 150)
        self.importance_trigger_curr = self.get_from_db(
            "importance_trigger_curr", self.importance_trigger_max
        )
        self.importance_ele_n = self.get_from_db("importance_ele_n", 0)
        self.thought_count = self.get_from_db("thought_count", 5)

        # PERSONA PLANNING
        # <daily_req> is a list of various goals the persona is aiming to achieve
        # today.
        # e.g., ['Work on her paintings for her upcoming show',
        #        'Take a break to watch some TV',
        #        'Make lunch for herself',
        #        'Work on her paintings some more',
        #        'Go to bed early']
        # They have to be renewed at the end of the day, which is why we are
        # keeping track of when they were first generated.
        self.daily_req = self.get_from_db("daily_req", [])
        # <f_daily_schedule> denotes a form of long term planning. This lays out
        # the persona's daily plan.
        # Note that we take the long term planning and short term decomposition
        # appoach, which is to say that we first layout hourly schedules and
        # gradually decompose as we go.
        # Three things to note in the example below:
        # 1) See how "sleeping" was not decomposed -- some of the common events
        #    really, just mainly sleeping, are hard coded to be not decomposable.
        # 2) Some of the elements are starting to be decomposed... More of the
        #    things will be decomposed as the day goes on (when they are
        #    decomposed, they leave behind the original hourly action description
        #    in tact).
        # 3) The latter elements are not decomposed. When an event occurs, the
        #    non-decomposed elements go out the window.
        # e.g., [['sleeping', 360],
        #         ['wakes up and ... (wakes up and stretches ...)', 5],
        #         ['wakes up and starts her morning routine (out of bed )', 10],
        #         ...
        #         ['having lunch', 60],
        #         ['working on her painting', 180], ...]
        self.f_daily_schedule = self.get_from_db("f_daily_schedule", [])
        # <f_daily_schedule_hourly_org> is a replica of f_daily_schedule
        # initially, but retains the original non-decomposed version of the hourly
        # schedule.
        # e.g., [['sleeping', 360],
        #        ['wakes up and starts her morning routine', 120],
        #        ['working on her painting', 240], ... ['going to bed', 60]]
        self.f_daily_schedule_hourly_org = self.get_from_db(
            "f_daily_schedule_hourly_org", []
        )
        # CURR ACTION
        # <address> is literally the string address of where the action is taking
        # place.  It comes in the form of
        # "{world}:{sector}:{arena}:{game_objects}". It is important that you
        # access this without doing negative indexing (e.g., [-1]) because the
        # latter address elements may not be present in some cases.
        # e.g., "dolores double studio:double studio:bedroom 1:bed"
        self.act_address = self.get_from_db("act_address")
        # <start_time> is a python datetime instance that indicates when the
        # action has started.
        self.act_step = self.get_from_db("act_step", None)
        if self.act_step is not None:
            self.act_start_time = self.from_step_to_time(self.act_step)
        else:
            self.act_start_time = None
        # <duration> is the integer value that indicates the number of minutes an
        # action is meant to last.
        self.act_duration = self.get_from_db("act_duration")
        # <description> is a string description of the action.
        self.act_description = self.get_from_db("act_description")
        # <pronunciatio> is the descriptive expression of the self.description.
        # Currently, it is implemented as emojis.
        self.act_pronunciatio = self.get_from_db("act_pronunciatio")
        # <event_form> represents the event triple that the persona is currently
        # engaged in.
        self.act_event = self.get_act_event()
        # <obj_description> is a string description of the object action.
        self.act_obj_description = self.get_from_db("act_obj_description")
        # <obj_pronunciatio> is the descriptive expression of the object action.
        # Currently, it is implemented as emojis.
        self.act_obj_pronunciatio = None
        self.act_obj_pronunciation = self.get_from_db("act_obj_pronunciation")
        # <obj_event_form> represents the event triple that the action object is
        # currently engaged in.
        self.act_obj_event = tuple(
            self.get_from_db("act_obj_event", (self.name, None, None))
        )
        # <chatting_with> is the string name of the persona that the current
        # persona is chatting with. None if it does not exist.
        self.chatting_with = self.get_from_db("chatting_with")
        # <chat> is a list of list that saves a conversation between two personas.
        # It comes in the form of: [["Dolores Murphy", "Hi"],
        #                           ["Maeve Jenson", "Hi"] ...]
        self.chat = None
        self.chat = self.get_from_db("chat")
        # <chatting_with_buffer>
        # e.g., ["Dolores Murphy"] = self.vision_r

        self.chatting_with_buffer = self.get_from_db("chatting_with_buffer", dict())
        self.chatting_end_step = self.get_from_db("chatting_end_step")
        if self.chatting_end_step is not None:
            self.chatting_end_time = self.from_step_to_time(self.chatting_end_step)
        else:
            self.chatting_end_time = None

        # <path_set> is True if we've already calculated the path the persona will
        # take to execute this action. That path is stored in the persona's
        # scratch.planned_path.

        self.act_path_set = self.get_from_db("act_path_set", False)
        # <planned_path> is a list of x y coordinate tuples (tiles) that describe
        # the path the persona is to take to execute the <curr_action>.
        # The list does not include the persona's current tile, and includes the
        # destination tile.
        # e.g., [(50, 10), (49, 10), (48, 10), ...]
        self.planned_path = self.get_from_db("planned_path", [])

    def get_act_event(self):
        dict_from_db = self.get_from_db("act_event", {"subject": self.name, "predicate": None, "object": None})
        print(dict_from_db)
        return tuple((dict_from_db["subject"],dict_from_db["predicate"],dict_from_db["object"]))
    
    def from_step_to_time(self, step):
        curr_minute = (self.start_step + step) * self.time_per_step
        curr_time_delta = datetime.timedelta(minutes=curr_minute)
        epoch_time = datetime.datetime(2024, 4, 9)
        curr_time = epoch_time + curr_time_delta
        return curr_time

    def act_check_finished(self):
        if not self.act_address:
            return True

        if self.chatting_with:
            end_time = self.chatting_end_time
        else:
            x = self.act_start_time
            if x.second != 0:
                x = x.replace(second=0)
                x = x + datetime.timedelta(minutes=1)
            end_time = x + datetime.timedelta(minutes=self.act_duration)

        if end_time.strftime("%H:%M:%S") == self.curr_time.strftime("%H:%M:%S"):
            return True
        return False

    def get_str_iss(self):
        commonset = ""
        commonset += f"Name: {self.name}\n"
        commonset += f"Age: {self.age}\n"
        commonset += f"Innate traits: {self.innate}\n"
        commonset += f"Learned traits: {self.learned}\n"
        commonset += f"Currently: {self.currently}\n"
        commonset += f"Lifestyle: {self.lifestyle}\n"
        commonset += f"Daily plan requirement: {self.daily_plan_req}\n"
        commonset += f"Current Date: {self.curr_time.strftime('%A %B %d')}\n"
        return commonset

    def get_f_daily_schedule_index(self, advance=0):
        today_min_elapsed = 0
        today_min_elapsed += self.curr_time.hour * 60
        today_min_elapsed += self.curr_time.minute
        today_min_elapsed += advance

        x = 0
        for task, duration in self.f_daily_schedule:
            x += duration
        x = 0
        for task, duration in self.f_daily_schedule_hourly_org:
            x += duration

        # We then calculate the current index based on that.
        curr_index = 0
        elapsed = 0
        for task, duration in self.f_daily_schedule:
            elapsed += duration
            if elapsed > today_min_elapsed:
                return curr_index
            curr_index += 1

        return curr_index

    def add_new_action(
        self,
        action_address,
        action_duration,
        action_description,
        action_pronunciatio,
        action_event,
        chatting_with,
        chat,
        chatting_with_buffer,
        chatting_end_time,
        act_obj_description,
        act_obj_pronunciatio,
        act_obj_event,
        act_start_time=None,
    ):
        self.act_address = action_address
        self.act_duration = action_duration
        self.act_description = action_description
        self.act_pronunciatio = action_pronunciatio
        self.act_event = action_event

        self.chatting_with = chatting_with
        self.chat = chat
        if chatting_with_buffer:
            self.chatting_with_buffer.update(chatting_with_buffer)
        self.chatting_end_time = chatting_end_time

        self.act_obj_description = act_obj_description
        self.act_obj_pronunciatio = act_obj_pronunciatio
        self.act_obj_event = act_obj_event

        self.act_start_time = self.curr_time

        self.act_path_set = False
