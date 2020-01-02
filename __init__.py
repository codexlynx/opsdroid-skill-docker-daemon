from opsdroid.skill import Skill
from opsdroid.matchers import match_parse
import docker


class DockerDaemonSkill(Skill):

    def blacklist(self):
        blacklist = self.config.get('containers-blacklist', [])
        if blacklist is None:
            return []
        return blacklist

    def docker_client(self):
        return docker.DockerClient(base_url=self.config['daemon-url'])

    def list_containers(self):
        client = self.docker_client()
        for container in client.containers.list():
            if container.name not in self.blacklist():
                yield container

    def get_container(self, message):
        client = self.docker_client()
        container_id = message.parse_result['container_id']
        container = client.containers.get(container_id)
        return container

    @match_parse('/docker_ps')
    async def ps(self, message):
        for container in self.list_containers():
            msg = 'Container ID: %s\nImage: %s\nNames: %s\n\n/docker_logs@%s\n' \
                  '/docker_restart@%s\n/docker_stop@%s' % (
                container.short_id,
                container.image.tags[0],
                container.name,
                container.short_id,
                container.short_id,
                container.short_id
            )
            await message.respond(msg)

    @match_parse('/docker_restart@{container_id}')
    async def restart(self, message):
        container = self.get_container(message)
        container.restart()
        await message.respond('Container: %s restarted!' % container.short_id)

    @match_parse('/docker_stop@{container_id}')
    async def stop(self, message):
        container = self.get_container(message)
        container.stop()
        await message.respond('Container: %s stopped!' % container.short_id)

    @match_parse('/docker_logs@{container_id}')
    async def logs(self, message):
        container = self.get_container(message)
        for line in container.logs().decode('utf8').splitlines():
            await message.respond(line)


