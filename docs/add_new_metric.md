# How to add a new metric

## metrics/version_metrics_name.py
### DataType
Add **new data** type with the **name of the file** you want to include.
```
    class DataType(Enum):
        <NewDataType> = <file_name>
        HalsteadDataType = "halstead"
```
    
### DataName
Add the **data name** related to the metric you want to include.
The current column name is the column name of the raw dataset you are extracting the metric.
```
    class DataName(Enum):
        <NewDataName> = auto(), DataType.<NewDataType>.value, <current_column_name>
        MultifacetedAbstraction = auto(), DataType.DesigniteDesignSmellsDataType.value, "Multifaceted Abstraction"
```

## metrics/version_metrics_data.py
### Extend Data
Create a new data class related to your metric that extends the Data class.
It must implement the **constructor** and the **build method**.
The build method must have in mind that the input df can have as **key features**: File, Package, Class and Method.
You must extract them from the dict format: <file>@<package>.<class>.<method>(<parameters>), and create columns with the specific names.
These will be in a column named 'id'. You need to drop it.

```
    class <NewMetric>Data(Data):
        def __init__(self, project, version, data=None):
            self.data_type = DataType.<NewDataType>.value
            self.raw_data = data
            super().__init__(project, version)

        def build(self, values, column_names):
            df = super().build(values, column_names)
            <implement the df based on the dictionary that you receive>
            df = df.drop(columns='id')
            df = df.rename(columns=column_names)
            return df
```

### CompositeData
You have to **append the new data class** you created to the **composite** of all metrics.

```
    def add_all(self, project, version):
        self.add(<NEW Data Class>(project, version))
```

## config.ini
### [EXTERNALS]
You should add the runner for the extractor, which may be useful later on to execute the specific code to get the metric.
For example, if you need to get Designite smells which is a Jar. Then, you assign in the externals Designite = DesigniteJava.jar
With this, in the Extractor you will easily be able to use the runner.

```
    [EXTERNALS]
    <runner_id> = <runner_value>
    Designite = DesigniteJava.jar
    SourceMonitor = SourceMonitor.exe
```

## metrics/version_metrics.py
### Extractor
Create a new Metric extractor that extends Extractor.
It should implement the **constructor** and the method **extract**.
The store will save the dataset in the following file:
    repository_mining/repository_data/metrics/<project_name>/<version_name>/<metric_name>.csv
```
    class <NewMetric>(Extractor):
        def __init__(self, project: Project, version):
            super().__init__("<runner_id>", project, version)

        def extract(self):
            <Implement the extract method so that you can get a dictionary of dictionaries>
            <This dictionary should have as key the file id and as values dictionaries with the metric_names as keys>
            <then, for each key a value corresponding to the metric value>
            <The file id is something of the nature <file_path>@<package>.<class>.<method>(<parameters>)>
            data = {<file_id>:{column_1: metric_1, column_2: metric_2}}
            self.data = <NewData>(self.project_name, self.version, data=data)
            self.data.store()
```