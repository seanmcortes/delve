from cx_Freeze import setup, Executable

buildOptions = dict(include_files = ['enemy.py',
                                     'helper.py',
                                     'map.py',
                                     'menu.py',
                                     'scenes.py',
                                     'settings.py',
                                     'sprites.py',
                                     'item.py',
                                     'image/',
                                     'maps/',
                                     'save/'])

setup(
    name = 'delve',
    version = '0.1',
    description = 'A game about delving.',
    author = 'Jason Anderson, Sean Cortes, Joshua Nutt',
    options = dict(build_exe = buildOptions),
    executables = [Executable('main.py')]
)

# Sources:
# https://stackoverflow.com/questions/15079268/how-can-i-include-a-folder-with-cx-freeze
# https://www.youtube.com/watch?v=EY6ZCPxqEtM