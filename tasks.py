from invoke import task


@task
def requirements(ctx):
    ctx.run("pip-compile --rebuild --no-annotate requirements.in")
    ctx.run("pip-compile --rebuild --no-annotate requirements_dev.in")
