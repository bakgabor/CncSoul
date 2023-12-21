from app.gui.gui_generator import GuiGenerator
from app.service.service_container import ServiceContainer


container = ServiceContainer()

gui_generator: GuiGenerator = container.get('gui_generator')
gui_generator.generate()
