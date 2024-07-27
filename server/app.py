# -*- coding: utf-8 -*-
# Copyright 2021 The Dapr Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os
import sys

from dapr.actor.runtime.config import ActorRuntimeConfig, ActorTypeConfig, ActorReentrancyConfig
from dapr.actor.runtime.runtime import ActorRuntime
from flask_dapr.actor import DaprActor
from flask import render_template, Flask

from smartbulb_actor import SmartBulbActor

app = Flask(f'{SmartBulbActor.__name__}Service')

# This is an optional advanced configuration which enables reentrancy only for the
# specified actor type. By default reentrancy is not enabled for all actor types.
config = ActorRuntimeConfig()  # init with default values
config.update_actor_type_configs([ActorTypeConfig(actor_type=SmartBulbActor.__name__,
                                                  reentrancy=ActorReentrancyConfig(enabled=True))])
ActorRuntime.set_actor_config(config)

# Add Dapr Actor Extension
actor = DaprActor(app)


def startup():
    print('-=-=-=-=-=-=-=Startup=-=-=-=-=-=-=-=-=', flush=True)
    actor.register_actor(SmartBulbActor)


@app.route('/')
def index():
    namespace = os.getenv('NAMESPACE') or 'default'
    return namespace
    # return render_template('index.html', namespace=namespace)


if __name__ == '__main__':
    startup()
    app.run(debug=True, port=5000)
