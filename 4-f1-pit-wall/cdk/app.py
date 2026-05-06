#!/usr/bin/env python3
"""F1 Pit Wall — CDK Application Entry Point."""

import aws_cdk as cdk
from stacks.infra_stack import InfraStack
from stacks.agent_stack import AgentStack
from stacks.frontend_stack import FrontendStack

app = cdk.App()

env = cdk.Environment(region="us-west-2")

infra = InfraStack(app, "F1PitWall-Infra", env=env)
agent = AgentStack(app, "F1PitWall-Agent", infra=infra, env=env)
frontend = FrontendStack(app, "F1PitWall-Frontend", agent=agent, env=env)

agent.add_dependency(infra)
frontend.add_dependency(agent)

app.synth()
