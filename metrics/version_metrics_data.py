from abc import ABC, abstractmethod


class Data(ABC):
    @abstractmethod
    def store(self):
        pass


class CompositeData(Data):
    def __init__(self):
        self.data_collection = []

    def store(self):
        for data in self.data_collection:
            data.store()

    def add(self, data):
        self.data_collection.append(data)


class CheckstyleData(Data):
    pass


class DesigniteData(Data):
    pass


class DesigniteImplementationSmellsData(DesigniteData):
    pass


class DesigniteDesignSmellsData(DesigniteData):
    pass


class DesigniteOrganicTypeSmellsData(DesigniteData):
    pass


class DesigniteOrganicMethodSmellsData(DesigniteData):
    pass


class DesigniteTypeMetricsData(DesigniteData):
    pass


class DesigniteMethodMetricsData(DesigniteData):
    pass


class SourceMonitorData(Data):
    pass


class SourceMonitorFilesData(SourceMonitorData):
    pass


class SourceMonitorMetricsData(SourceMonitorData):
    pass


class CKData(Data):
    pass


class MoodData(Data):
    pass


class HalsteadData(Data):
    pass
