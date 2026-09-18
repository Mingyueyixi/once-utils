from ._resource import Res
import json

from onceutils.analysis.groovy import GroovyScript
from onceutils.analysis.groovy import GroovyBlock



def test_groovy_script():
    groovy_script = GroovyScript(Res.data_path("build.test.gradle"))
    buildscript = groovy_script.root.find("buildscript")
    assert buildscript
    assert buildscript.text.startswith("buildscript {")
    assert not buildscript.content.startswith("buildscript {")
    block_repositories = groovy_script.root.find("repositories")
    child_repositories = block_repositories.child_names
    assert "maven" in child_repositories
    assert "google" in child_repositories
    for child in block_repositories.children:
        child:GroovyBlock
        if child.name == "maven":
            assert "url" in child.content
            assert child.text.startswith("maven {")
        if child.name == "google":
            assert "url" not in child.content
            assert "includeGroupByRegex" in child.content





