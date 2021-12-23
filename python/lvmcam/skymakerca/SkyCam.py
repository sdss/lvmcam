from skymakercam.camera import SkymakerCameraSystem, SkymakerCamera


class SkyCameraSystem(SkymakerCameraSystem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_available_cameras(self):
        """ Gather skymaker camera uids.
        :return: a list of cameras.
        :rtype: list
        """
        available_uid_list = []
        for _, val in self._config.items():
            try:
                # print(key, val['type'], val['uid'])
                if val['type'] == 'skymakercam':
                    available_uid_list.append(val['uid'])
            except KeyError:
                pass
        return available_uid_list


class SkyCamera(SkymakerCamera):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _disconnect_internal(self):
        await self.amqpc.stop()
