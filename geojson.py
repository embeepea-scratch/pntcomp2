import pnt

class FeatureCollection:
    def __init__(self):
        self.features = []
    def toString(self):
        lines = []
        lines.append('{"type": "FeatureCollection","features":[')
        lines.append(",".join( [feature.toString() for feature in self.features] ))
        lines.append("]}")
        return "".join(lines)

class MultiPolygonFeature:
    def __init__(self, id, name, polygons):
        self.id = id
        self.name = name
        self.polygons = polygons
    def toString(self):
        g = pnt.PntGrid()
        lines = []
        lines.append('{"type":"Feature","id":"%s",' % self.id)
        lines.append('"properties":{"name":"%s"},' % self.name)
        lines.append('"geometry":{"type":"MultiPolygon","coordinates":[')
        lines.append(
            ",".join(
                ("[[" + ",".join(["[%.2f,%.2f]" % (g.xTr.int_to_float(p[0]), g.yTr.int_to_float(p[1])) for p in polygon]) + "]]")
                for polygon in self.polygons
            )
        )
        lines.append("]}}")
        return "".join(lines)
