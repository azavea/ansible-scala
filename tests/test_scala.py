import pytest


@pytest.fixture()
def AnsibleDefaults(Ansible):
    """ Load default variables into dictionary.

    Args:
        Ansible - Requires the ansible connection backend.
    """
    return Ansible("include_vars", "./defaults/main.yml")["ansible_facts"]


@pytest.fixture()
def AnsibleFacts(Ansible):
    """ Load ansible facts into a dictionary.

    Args:
        Ansible - Requires ansible connection backend.
    """

    return Ansible("setup")["ansible_facts"]


def test_java_exists(AnsibleFacts, Package):
    """ Ensure that the proper java version has been installed

    Args:
        AnsibleFacts - Dictionary of Ansible facts.
        Package - Module that gives information about package install status
            and version.

    Raises:
        AssertionError if the wrong java version is installed.
    """

    # Ubuntu 16.04 and above only support openjdk 8
    os_version = AnsibleFacts["ansible_distribution_version"]
    if float(os_version) >= 16.04:
        java_major_version = "8"
    else:
        java_major_version = "7"

    assert Package("openjdk-{}-jdk".format(java_major_version)).is_installed


def test_scala_exists(Command):
    """ Attempt to run the scala binary to ensure it exists.

    Args:
        Command - module to run commands in a remote shell.

    Raises:
        AssertionError if the command's return code is not zero.
    """
    Command.run_test(
        "scala -e \"println(util.Properties.versionNumberString)\"")


def test_scala_version(Command, AnsibleDefaults):
    """ Check that Ansible installed the proper version of scala

    Args:
         Command - module to run commands in a remote shell.
         AnsibleDefaults - Dictionary of default ansible variable values.

    Raises:
        AssertionError if the command's return code is not zero.
    """
    # Extract target scala version from ansible facts
    target_scala_version = AnsibleDefaults["scala_version"]

    # Ensure that the running version of scala is the target version
    Command.run_test(
        "scala -e \"println(util.Properties.versionNumberString)\" |"
        " grep {}".format(target_scala_version))


def test_sbt(Package, AnsibleDefaults):
    """ Check to see if the proper version of SBT is installed.

    Args:
        Package: module that verifies package install and version
        AnsibleDefaults - Dictionary of default ansible variable values.

    Raises:
        AssertionError if the proper version of SBT isn't installed, or SBT
            is installed at the wrong version.
    """
    target_sbt_version = AnsibleDefaults["scala_sbt_version"]
    installed_version = Package("sbt").version
    assert Package("sbt").is_installed
    assert installed_version.startswith(target_sbt_version)
