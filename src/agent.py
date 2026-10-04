import json
from datetime import date, timedelta

from google import genai

from src.tools import TOOLS


# --------------------------------------------------
# GEMINI
# --------------------------------------------------

client = genai.Client()

MODEL = "gemini-3.5-flash-lite"


# --------------------------------------------------
# TEMPORARY AGENT STATE
# --------------------------------------------------

# Stores actions waiting for confirmation.
#
# Example:
#
# PENDING_ACTIONS[1] = {
#     "tool_name": "delete_expense",
#     "arguments": {
#         "expense_id": 8
#     }
# }

PENDING_ACTIONS = {}


# --------------------------------------------------
# TOOL DEFINITIONS
# --------------------------------------------------

TOOL_DEFINITIONS = [

    {
        "type": "function",
        "name": "add_expense",
        "description": "Add a confirmed expense.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number"
                },
                "category": {
                    "type": "string"
                },
                "date": {
                    "type": "string",
                    "description": "YYYY-MM-DD"
                }
            },
            "required": [
                "amount",
                "category",
                "date"
            ]
        }
    },

    {
        "type": "function",
        "name": "get_expenses",
        "description": (
            "Get all expenses for the current user. "
            "Use this before updating or deleting an expense "
            "when the user refers to an expense by amount, "
            "category, date, or words like 'that expense'."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },

    {
        "type": "function",
        "name": "update_expense",
        "description": (
            "Update an expense by its ID. "
            "Requires confirmation from the user before execution."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expense_id": {
                    "type": "integer"
                },
                "amount": {
                    "type": "number"
                }
            },
            "required": [
                "expense_id",
                "amount"
            ]
        }
    },

    {
        "type": "function",
        "name": "delete_expense",
        "description": (
            "Delete an expense by its ID. "
            "Requires confirmation from the user before execution."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expense_id": {
                    "type": "integer"
                }
            },
            "required": [
                "expense_id"
            ]
        }
    },

    {
        "type": "function",
        "name": "add_income",
        "description": "Add confirmed income.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number"
                },
                "source": {
                    "type": "string"
                },
                "date": {
                    "type": "string",
                    "description": "YYYY-MM-DD"
                }
            },
            "required": [
                "amount",
                "source",
                "date"
            ]
        }
    },

    {
        "type": "function",
        "name": "get_income",
        "description": "Get the user's income records.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },

    {
        "type": "function",
        "name": "update_income",
        "description": (
            "Update income by its ID. "
            "Requires confirmation from the user before execution."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "income_id": {
                    "type": "integer"
                },
                "amount": {
                    "type": "number"
                }
            },
            "required": [
                "income_id",
                "amount"
            ]
        }
    },

    {
        "type": "function",
        "name": "delete_income",
        "description": (
            "Delete income by its ID. "
            "Requires confirmation from the user before execution."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "income_id": {
                    "type": "integer"
                }
            },
            "required": [
                "income_id"
            ]
        }
    },

    {
        "type": "function",
        "name": "get_balance",
        "description": "Get the current confirmed balance.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },

    {
        "type": "function",
        "name": "get_daily_summary",
        "description": "Get confirmed expenses for a specific date.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "YYYY-MM-DD"
                }
            },
            "required": [
                "date"
            ]
        }
    },

    {
        "type": "function",
        "name": "get_weekly_summary",
        "description": "Get confirmed expenses between two dates.",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string"
                },
                "end_date": {
                    "type": "string"
                }
            },
            "required": [
                "start_date",
                "end_date"
            ]
        }
    },

    {
        "type": "function",
        "name": "get_monthly_summary",
        "description": "Get confirmed expenses between two dates.",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string"
                },
                "end_date": {
                    "type": "string"
                }
            },
            "required": [
                "start_date",
                "end_date"
            ]
        }
    },

    {
        "type": "function",
        "name": "get_yearly_summary",
        "description": "Get confirmed expenses between two dates.",
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string"
                },
                "end_date": {
                    "type": "string"
                }
            },
            "required": [
                "start_date",
                "end_date"
            ]
        }
    }
]


# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------

def get_system_instruction():

    today = date.today()
    yesterday = today - timedelta(days=1)

    return f"""
You are a personal expense assistant.

Today is {today.isoformat()}.
Yesterday was {yesterday.isoformat()}.

Currency: INR.

Rules:

- Always use ₹ for money.
- Never invent financial data.
- Never invent amounts.
- Never invent dates.
- "today" means {today.isoformat()}.
- "yesterday" means {yesterday.isoformat()}.
- Use tools for financial data.
- Adding expenses/income can happen immediately.
- Updating/deleting requires confirmation.
- If the user refers to an existing expense or income
  without giving its ID, first use the appropriate
  get tool to find the record.
- If multiple records could match, ask the user to
  clarify which one they mean.
- Never guess an ID.
- Never execute update or delete directly.
- The application will ask the user for confirmation.
- Keep answers short and natural.
"""


# --------------------------------------------------
# ARGUMENT PREPARATION
# --------------------------------------------------

def prepare_arguments(tool_name, arguments, user_id):

    args = dict(arguments)

    # user_id is controlled by the application.
    # Never allow Gemini to choose it.
    args["user_id"] = user_id

    if tool_name == "add_expense":
        args["expense_date"] = args.pop("date")

    elif tool_name == "add_income":
        args["income_date"] = args.pop("date")

    return args


# --------------------------------------------------
# TOOL EXECUTION
# --------------------------------------------------

def execute_tool(tool_name, arguments, user_id):

    function = TOOLS.get(tool_name)

    if function is None:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}"
        }

    args = prepare_arguments(
        tool_name,
        arguments,
        user_id
    )

    try:

        result = function(**args)

        if result is None:
            return {
                "success": True
            }

        if isinstance(result, (int, float, str, list, tuple)):
            return {
                "success": True,
                "data": result
            }

        if isinstance(result, dict):
            return result

        return {
            "success": True,
            "data": str(result)
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }

# --------------------------------------------------
# CHECK CONFIRMATION
# --------------------------------------------------

def is_confirmation(message):

    text = message.strip().lower()

    yes_words = {
        "yes",
        "y",
        "yeah",
        "yep",
        "yup",
        "yas",
        "yess",
        "sure",
        "confirm",
        "confirmed",
        "do it",
        "go ahead",
        "okay",
        "ok"
    }

    no_words = {
        "no",
        "n",
        "nope",
        "cancel",
        "cancel it",
        "don't",
        "do not"
    }

    if text in yes_words:
        return True

    if text in no_words:
        return False

    return None



# --------------------------------------------------
# EXECUTE PENDING ACTION
# --------------------------------------------------

def execute_pending_action(user_id):

    action = PENDING_ACTIONS.get(user_id)

    if action is None:
        return None

    tool_name = action["tool_name"]
    arguments = action["arguments"]

    result = execute_tool(
        tool_name,
        arguments,
        user_id
    )

    # Always clear the pending action after an attempt.
    del PENDING_ACTIONS[user_id]

    if not result.get("success"):

        return (
            f"I couldn't complete the action: "
            f"{result.get('error', 'Unknown error')}"
        )

    if tool_name == "delete_expense":

        expense_id = arguments["expense_id"]

        return (
            f"Done. Expense #{expense_id} was deleted."
        )

    if tool_name == "delete_income":

        income_id = arguments["income_id"]

        return (
            f"Done. Income #{income_id} was deleted."
        )

    if tool_name == "update_expense":

        expense_id = arguments["expense_id"]
        amount = arguments["amount"]

        return (
            f"Done. Expense #{expense_id} was updated "
            f"to ₹{amount}."
        )

    if tool_name == "update_income":

        income_id = arguments["income_id"]
        amount = arguments["amount"]

        return (
            f"Done. Income #{income_id} was updated "
            f"to ₹{amount}."
        )

    return "Done."


# --------------------------------------------------
# MAIN AGENT
# --------------------------------------------------

def run_agent(user_message, user_id):

    # --------------------------------------------------
    # CHECK FOR PENDING CONFIRMATION
    # --------------------------------------------------

    if user_id in PENDING_ACTIONS:

        confirmation = is_confirmation(user_message)

        if confirmation is True:
            return execute_pending_action(user_id)

        if confirmation is False:

            del PENDING_ACTIONS[user_id]

            return "Cancelled. Nothing was changed."

        return (
            "Please answer yes to confirm "
            "or no to cancel."
        )

    # --------------------------------------------------
    # INITIAL GEMINI REQUEST
    # --------------------------------------------------

    try:

        interaction = client.interactions.create(

            model=MODEL,

            input=user_message,

            tools=TOOL_DEFINITIONS,

            system_instruction=get_system_instruction()
        )

    except Exception as error:

        print("GEMINI ERROR:", error)

        return (
            "Gemini is temporarily unavailable. "
            "Please try again."
        )

    # --------------------------------------------------
    # AGENT LOOP
    # --------------------------------------------------

    # Prevent an accidental infinite tool loop.
    MAX_TOOL_ROUNDS = 10

    for _ in range(MAX_TOOL_ROUNDS):

        function_calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        # --------------------------------------------------
        # NO TOOL CALL
        # --------------------------------------------------

        if not function_calls:

            return interaction.output_text

        # --------------------------------------------------
        # PROCESS FUNCTION CALLS
        # --------------------------------------------------

        function_results = []

        for step in function_calls:

            tool_name = step.name
            arguments = step.arguments

            print(
                f"AI tool: {tool_name}"
            )

            print(
                f"Arguments: {arguments}"
            )

            # --------------------------------------------------
            # UPDATE / DELETE
            # --------------------------------------------------

            if tool_name in {
                "update_expense",
                "delete_expense",
                "update_income",
                "delete_income"
            }:

                # Store the action WITHOUT executing it.
                PENDING_ACTIONS[user_id] = {
                    "tool_name": tool_name,
                    "arguments": arguments
                }

                if tool_name == "delete_expense":

                    expense_id = arguments["expense_id"]

                    return (
                        f"I found expense #{expense_id}. "
                        f"Are you sure you want to delete it?"
                    )

                if tool_name == "delete_income":

                    income_id = arguments["income_id"]

                    return (
                        f"I found income #{income_id}. "
                        f"Are you sure you want to delete it?"
                    )

                if tool_name == "update_expense":

                    expense_id = arguments["expense_id"]
                    amount = arguments["amount"]

                    return (
                        f"I found expense #{expense_id}. "
                        f"Do you want to change it to ₹{amount}?"
                    )

                if tool_name == "update_income":

                    income_id = arguments["income_id"]
                    amount = arguments["amount"]

                    return (
                        f"I found income #{income_id}. "
                        f"Do you want to change it to ₹{amount}?"
                    )

            # --------------------------------------------------
            # NORMAL TOOL
            # --------------------------------------------------

            result = execute_tool(
                tool_name,
                arguments,
                user_id
            )

            print(
                f"Tool result: {result}"
            )

            # --------------------------------------------------
            # PREPARE RESULT FOR GEMINI
            # --------------------------------------------------

            function_results.append(
                {
                    "type": "function_result",
                    "name": tool_name,
                    "call_id": step.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(
                                result,
                                default=str
                            )
                        }
                    ]
                }
            )

        # --------------------------------------------------
        # SEND ALL TOOL RESULTS BACK TO GEMINI
        # --------------------------------------------------

        try:

            interaction = client.interactions.create(

                model=MODEL,

                previous_interaction_id=interaction.id,

                input=function_results,

                tools=TOOL_DEFINITIONS,

                system_instruction=get_system_instruction()
            )

        except Exception as error:

            print(
                "GEMINI RESULT ERROR:",
                error
            )

            return (
                "I completed the tool operation, "
                "but couldn't generate the final response."
            )

    # --------------------------------------------------
    # TOOL LOOP LIMIT
    # --------------------------------------------------

    return (
        "I couldn't complete that request because "
        "the agent reached its tool-call limit."
    )

