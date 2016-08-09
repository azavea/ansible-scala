def test_java_exists(Command):
	java = Command("java -version")
	assert java.rc == 0


def test_scala_exists(Command, Ansible, SystemInfo):
	scala_version = Command(
		"scala -e \"println(util.Properties.versionNumberString)\"")
	assert scala_version.rc == 0

def test_scala_version(Command, Sudo):
	with Sudo(user='root'):
		# Extract target scala version from ansible facts
		target_scala_version = Command.check_output(
			"cat /etc/ansible/facts.d/molecule.fact"
			" | grep target_scala_version | cut -f2 -d'='")

		# Ensure that the running version of scala is the target version
		Command.run_test(
			"scala -e \"println(util.Properties.versionNumberString)\" |"
			" grep %s" % target_scala_version)

		# Extract target sbt version from ansible facts
		target_sbt_version = Command.check_output(
			"cat /etc/ansible/facts.d/molecule.fact |"
			" grep target_sbt_version | cut -f2 -d'='")

		# Ensure that the running version of sbt is the target version
		Command.run_test("sbt sbtVersion | grep %s" % target_sbt_version)