from opsdroid.skill import Skill
from opsdroid.matchers import match_parse
import docker


class DockerDaemonSkill(Skill):

    @match_parse('/docker_ps')
    async def ps(self, message):
        client = docker.DockerClient(base_url=self.config['daemon-url'])
        for container in client.containers.list():
            if container.name not in self.config['containers-blacklist']:
                msg = 'Container ID: %s\nImage: %s\nNames: %s\n\n/docker_restart_%s\n/docker_stop_%s' % (
                    container.short_id,
                    container.image.tags[0],
                    container.name,
                    container.short_id,
                    container.short_id
                )
                await message.respond(msg)

    @match_parse('/docker_restart_{container_id}')
    async def restart(self, message):
        client = docker.DockerClient(base_url=self.config['daemon-url'])
        container_id = message.parse_result['container_id']
        container = client.containers.get(container_id)
        container.restart()
        await message.respond('Container: %s restarted!' % container_id)

    @match_parse('/docker_stop_{container_id}')
    async def stop(self, message):
        client = docker.DockerClient(base_url=self.config['daemon-url'])
        container_id = message.parse_result['container_id']
        container = client.containers.get(container_id)
        container.stop()
        await message.respond('Container: %s stopped!' % container_id)
