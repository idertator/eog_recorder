clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf
	rm -rf ./saccrec.egg-info

sonar:
	sonar-scanner \
	  -Dsonar.projectKey=eog_recorder \
	  -Dsonar.sources=./saccrec \
	  -Dsonar.exclusions=data/** \
	  -Dsonar.inclusions=**/*.py \
	  -Dsonar.python.version=3.11 \
	  -Dsonar.host.url=http://localhost:9001 \
	  -Dsonar.login=sqp_ec8d730d9b4c021f54f45102a855770b124846c3

format:
	black ./saccrec

tags::
	ctags -R .
