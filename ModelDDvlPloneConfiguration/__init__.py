import ModelDDvlPloneConfiguration

def initialize(context):

    "This makes the tool apear in the product list"

    context.registerClass(
        ModelDDvlPloneConfiguration.ModelDDvlPloneConfiguration,
        constructors = ModelDDvlPloneConfiguration.constructors,
        icon="skins/ModelDDvlPloneConfiguration_icon.gif"
    )
