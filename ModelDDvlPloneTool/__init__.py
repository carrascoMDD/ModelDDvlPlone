import ModelDDvlPloneTool

def initialize(context):

    "This makes the tool apear in the product list"

    context.registerClass(
        ModelDDvlPloneTool.ModelDDvlPloneTool,
        constructors = ModelDDvlPloneTool.constructors,
        icon="skins/icon.gif"
    )
