.. # ********** Please don't edit this file!
.. # ********** It has been generated automatically by dae_devops version 0.5.4.dev0+g1fb30ef.d20230527.
.. # ********** For repository_name dls-utilpack

Devops
=======================================================================

In the top level of the repository there exists a configuration file called ``.dae-devops/project.yaml``.

This file defines the project information needed for CI/CD.

It is parsed by the ``dae_devops.force`` command which creates these files:

- pyproject.toml
- .githib/*
- .gitlab-ci.yml
- .dae-devops/Makefile
- .dae-devops/docs/*

Local CI/CD execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All the CI/CD ops which are run by the git server can be run at the command line.

Running these ops before pushing to the git server can make the turnaround quicker to fix things.

Follow the steps in the Developing section.  Then you can run the following commands.

Validation of the code::

    $ make -f .dae-devops/Makefile validate_pre_commit
    $ make -f .dae-devops/Makefile validate_mypy
    $ make -f .dae-devops/Makefile validate_pytest
    $ make -f .dae-devops/Makefile validate_docs

Packaging (for the Diamond intranet):: 

    $ make -f .dae-devops/Makefile package_pip

Publishing (for the Diamond intranet)::

    $ make -f .dae-devops/Makefile publish_pip
    $ make -f .dae-devops/Makefile publish_docs
    
The Diamond intranet commands are not used for production. The production packaging and publishing are handled in the GitHub Actions workflows mechanism.

.. # dae_devops_fingerprint 322b02a91652f7af8cf6b5fce4f890c7
