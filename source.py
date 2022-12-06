from rcwa.shorthand import *
from rcwa import freeSpaceLayer

class Source:
    """
    Class for defining monochromatic excitation source

    :param wavelength: The wavelength (in microns, or your preferred length unit due to the scale-invariance of Maxwell's equations.
    :param theta: Angle with respect to the vector normal to the layer stack, in radians
    :param phi: Rotation angle amount the vector normal to the layer stack
    :param pTEM: Polarization vector for TE/TM polarization fraction (can be complex)
    :param layer: Layer source is located in
    """
    def __init__(self, wavelength=2*pi,theta=0, phi=0, pTEM=[1,1], layer=freeSpaceLayer):
        self.freeSpaceWavelength=wavelength
        self.k0 = 2*pi / wavelength
        self.theta = theta
        self.phi = phi
        self.pTE = pTEM[0]
        self.pTM = pTEM[1]
        normalizationFactor = norm(np.array([self.pTE, self.pTM]))
        self.pTE /= normalizationFactor
        self.pTM /= normalizationFactor
        self.layer=layer
        self.setTEMVectors()
        self.setKIncident()
        self.pX = (self.pTE*self.aTE + self.pTM*self.aTM)[0]
        self.pY = (self.pTE*self.aTE + self.pTM*self.aTM)[1]

    def __eq__(self, other):
        if not isinstance(other, Source):
            return NotImplemented
        return self.freeSpaceWavelength == other.freeSpaceWavelength and \
                self.k0 == other.k0 and \
                self.theta == other.theta and \
                self.phi == other.phi and \
                self.pTE == other.pTE and \
                self.pTM == other.pTM and \
                self.pX == other.pX and \
                self.pY == other.pY and \
                self.kIncident == other.kIncident and \
                self.aTE == other.aTE and \
                self.aTM == other.aTM

    def __str__(self):
        return f'wavelength: {self.freeSpaceWavelength:.3f}, (theta, phi) = ({self.theta:.4f}, {self.phi:.4f})\n' + \
                f'kIncident: {self.kIncident}, polarization: ({self.pTE:.3f}, {self.pTM:.3f})\n' + \
                f'TEM vector: ({self.aTE}, {self.aTM})\n'

    def __repr__(self):
        return f'wavelength: {self.freeSpaceWavelength:.3f}, (theta, phi) = ({self.theta:.4f}, {self.phi:.4f})' + \
                f'kIncident: {self.kIncident}, polarization: ({self.pTE:.3f}, {self.pTM:.3f})' + \
                f'TEM vector: ({self.aTE}, {self.aTM})'

    def getRepresentationVector(self):
        return complexArray([self.wavelength, self.k0, self.theta, self.phi, self.pTE, self.pTM,
            self.pX, self.pY, self.kIncident[0], self.kIncident[1], self.kIncident[2],
            self.aTE[0], self.aTE[1], self.aTM[0], self.aTM[1]])


    @property
    def wavelength(self):
        if isinstance(self.freeSpaceWavelength, np.ndarray):
            return self.freeSpaceWavelength[0]
        else:
            return self.freeSpaceWavelength

    @wavelength.setter
    def wavelength(self, wavelength):
        self.freeSpaceWavelength = wavelength
        self.k0 = 2 * pi / wavelength
        self.setKIncident()

    def setTEMVectors(self):
        deviceNormalUnitVector = complexArray([0,0,-1]);
        epsilon = 1e-3;
        xComponent=  sin(self.theta) * cos(self.phi);
        yComponent = sin(self.theta) * sin(self.phi);
        zComponent = cos(self.theta);
        incidentVector = np.array([xComponent, yComponent, zComponent])

        if(abs(xComponent) < epsilon and abs(yComponent) < epsilon):
            self.aTE = np.array([0,1,0]);
        else:
            self.aTE = - np.cross(deviceNormalUnitVector, incidentVector);
            self.aTE = self.aTE / norm(self.aTE);

        self.aTM = (np.cross(self.aTE, incidentVector));
        self.aTM = (self.aTM / norm(self.aTM));
        self.ATEM = np.vstack((self.aTE, self.aTM)) # matrix that goes from x/y basis to TE/TM basis

    def setKIncident(self):
        n = sqrt(self.layer.er*self.layer.ur);
        kx = n * sin(self.theta) * cos(self.phi);
        ky = n * sin(self.theta) * sin(self.phi);
        kz = n * cos(self.theta);
        self.kIncident = complexArray([kx, ky, kz])

zeroSource = Source(float("inf"))
